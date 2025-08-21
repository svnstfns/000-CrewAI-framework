"""
Monitored Agent Wrapper
Enhances CrewAI agents with dashboard monitoring capabilities
"""

import time
import uuid
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass

from crewai import Agent, Task
from ..memory.qdrant_storage import QdrantMemoryManager
from ..dashboard.framework_bridge import CrewAIDashboardBridge


@dataclass
class AgentPerformance:
    """Agent performance tracking"""

    agent_id: str
    tasks_started: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_execution_time: float = 0.0
    average_response_time: float = 0.0
    last_task_time: Optional[datetime] = None
    current_task: Optional[str] = None
    status: str = "idle"  # idle, processing, error, completed


class MonitoredAgent:
    """Enhanced agent with monitoring capabilities"""

    def __init__(
        self,
        agent: Agent,
        memory_manager: QdrantMemoryManager,
        dashboard_bridge: Optional[CrewAIDashboardBridge] = None,
    ):
        """
        Initialize monitored agent

        Args:
            agent: CrewAI agent instance
            memory_manager: Qdrant memory manager
            dashboard_bridge: Dashboard bridge for metrics
        """
        self.agent = agent
        self.memory_manager = memory_manager
        self.dashboard_bridge = dashboard_bridge

        # Generate unique agent ID
        self.agent_id = f"{agent.role}_{uuid.uuid4().hex[:8]}"

        # Performance tracking
        self.performance = AgentPerformance(agent_id=self.agent_id)

        # Memory collections for this agent
        self.agent_memory = memory_manager.get_storage("agent_communication")
        self.code_memory = memory_manager.get_storage("code_snippets")
        self.debug_memory = memory_manager.get_storage("debugging_history")

        # Wrap original methods
        self._wrap_agent_methods()

        print(f"🤖 Monitored Agent initialized: {self.agent_id}")

    def _wrap_agent_methods(self):
        """Wrap agent methods with monitoring"""
        original_execute = self.agent.execute

        def monitored_execute(task: Task):
            """Execute task with monitoring"""
            task_id = f"task_{uuid.uuid4().hex[:8]}"
            start_time = time.time()

            # Update performance tracking
            self.performance.tasks_started += 1
            self.performance.current_task = (
                task.description[:50] + "..."
                if len(task.description) > 50
                else task.description
            )
            self.performance.status = "processing"
            self.performance.last_task_time = datetime.now()

            # Log task start
            self._log_task_start(task, task_id)

            # Update dashboard
            self._update_dashboard_status()

            try:
                # Execute task
                result = original_execute(task)

                # Calculate execution time
                execution_time = time.time() - start_time

                # Update performance
                self.performance.tasks_completed += 1
                self.performance.total_execution_time += execution_time
                self.performance.average_response_time = (
                    self.performance.total_execution_time
                    / self.performance.tasks_completed
                )
                self.performance.status = "completed"
                self.performance.current_task = None

                # Log successful completion
                self._log_task_completion(
                    task, task_id, result, execution_time, success=True
                )

                # Store in memory
                self._store_task_result(task, result, execution_time, success=True)

                return result

            except Exception as e:
                # Calculate execution time
                execution_time = time.time() - start_time

                # Update performance
                self.performance.tasks_failed += 1
                self.performance.status = "error"
                self.performance.current_task = None

                # Log error
                self._log_task_completion(
                    task, task_id, str(e), execution_time, success=False
                )

                # Store error in memory
                self._store_task_result(task, str(e), execution_time, success=False)

                # Store debugging info
                self._store_debug_info(task, e)

                raise e

        # Replace execute method
        self.agent.execute = monitored_execute

    def _log_task_start(self, task: Task, task_id: str):
        """Log task start"""
        log_data = {
            "event": "task_start",
            "task_id": task_id,
            "agent_id": self.agent_id,
            "task_description": task.description,
            "timestamp": datetime.now().isoformat(),
        }

        # Store in agent memory
        self.agent_memory.save(
            log_data,
            {
                "memory_type": "task_log",
                "agent_id": self.agent_id,
                "event_type": "start",
            },
        )

        print(f"🔄 [{self.agent_id}] Starting task: {task.description[:50]}...")

    def _log_task_completion(
        self,
        task: Task,
        task_id: str,
        result: Any,
        execution_time: float,
        success: bool,
    ):
        """Log task completion"""
        log_data = {
            "event": "task_completion",
            "task_id": task_id,
            "agent_id": self.agent_id,
            "task_description": task.description,
            "result": str(result)[:200] + "..."
            if len(str(result)) > 200
            else str(result),
            "execution_time": execution_time,
            "success": success,
            "timestamp": datetime.now().isoformat(),
        }

        # Store in agent memory
        self.agent_memory.save(
            log_data,
            {
                "memory_type": "task_log",
                "agent_id": self.agent_id,
                "event_type": "completion",
                "success": success,
            },
        )

        status = "✅" if success else "❌"
        print(f"{status} [{self.agent_id}] Task completed in {execution_time:.2f}s")

    def _store_task_result(
        self, task: Task, result: Any, execution_time: float, success: bool
    ):
        """Store task result in memory"""
        result_data = {
            "task_description": task.description,
            "result": str(result),
            "execution_time": execution_time,
            "success": success,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
        }

        # Store in appropriate memory collection
        if success:
            # Store successful patterns
            self.memory_manager.save_to_memory(
                "workflow_patterns",
                result_data,
                {
                    "pattern_type": "successful_task",
                    "agent_id": self.agent_id,
                    "execution_time": execution_time,
                },
            )
        else:
            # Store error patterns
            self.memory_manager.save_to_memory(
                "debugging_history",
                result_data,
                {"error_type": "task_execution", "agent_id": self.agent_id},
            )

    def _store_debug_info(self, task: Task, error: Exception):
        """Store debugging information"""
        debug_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "task_description": task.description,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "context": {
                "agent_role": self.agent.role,
                "agent_goal": self.agent.goal,
                "task_expected_output": getattr(task, "expected_output", "N/A"),
            },
        }

        # Store in debugging memory
        self.debug_memory.save(
            debug_data,
            {
                "memory_type": "error_pattern",
                "agent_id": self.agent_id,
                "error_type": type(error).__name__,
            },
        )

    def _update_dashboard_status(self):
        """Update dashboard with current agent status"""
        if not self.dashboard_bridge:
            return

        # Calculate resource usage (simulated)
        import psutil

        process = psutil.Process()

        status_data = {
            "name": self.agent.role,
            "status": self.performance.status,
            "tasks_completed": self.performance.tasks_completed,
            "tasks_failed": self.performance.tasks_failed,
            "current_task": self.performance.current_task,
            "cpu_usage": process.cpu_percent(),
            "memory_usage": process.memory_percent(),
            "response_time": self.performance.average_response_time,
        }

        self.dashboard_bridge.update_agent_status(self.agent_id, status_data)

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get agent performance summary"""
        total_tasks = self.performance.tasks_completed + self.performance.tasks_failed
        success_rate = (
            (self.performance.tasks_completed / total_tasks * 100)
            if total_tasks > 0
            else 0
        )

        return {
            "agent_id": self.agent_id,
            "role": self.agent.role,
            "total_tasks": total_tasks,
            "tasks_completed": self.performance.tasks_completed,
            "tasks_failed": self.performance.tasks_failed,
            "success_rate": success_rate,
            "average_response_time": self.performance.average_response_time,
            "total_execution_time": self.performance.total_execution_time,
            "current_status": self.performance.status,
            "last_activity": self.performance.last_task_time.isoformat()
            if self.performance.last_task_time
            else None,
        }

    def search_memory(
        self, query: str, memory_type: str = "agent_communication", limit: int = 5
    ) -> List[Dict]:
        """Search agent's memory"""
        return self.memory_manager.retrieve_from_memory(memory_type, query, limit)

    def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        """Get recent agent activities"""
        return self.search_memory("recent activities", "agent_communication", limit)

    def get_error_history(self, limit: int = 5) -> List[Dict]:
        """Get agent's error history"""
        return self.search_memory("error", "debugging_history", limit)

    def get_successful_patterns(self, limit: int = 5) -> List[Dict]:
        """Get successful task patterns"""
        return self.search_memory("successful", "workflow_patterns", limit)


class MonitoredCrew:
    """Enhanced crew with monitoring capabilities"""

    def __init__(
        self,
        agents: List[MonitoredAgent],
        tasks: List[Task],
        memory_manager: QdrantMemoryManager,
        dashboard_bridge: Optional[CrewAIDashboardBridge] = None,
    ):
        """
        Initialize monitored crew

        Args:
            agents: List of monitored agents
            tasks: List of tasks
            memory_manager: Qdrant memory manager
            dashboard_bridge: Dashboard bridge for metrics
        """
        self.agents = agents
        self.tasks = tasks
        self.memory_manager = memory_manager
        self.dashboard_bridge = dashboard_bridge

        # Crew performance tracking
        self.crew_id = f"crew_{uuid.uuid4().hex[:8]}"
        self.start_time = None
        self.end_time = None

        print(f"👥 Monitored Crew initialized: {self.crew_id}")

    async def execute(self) -> Dict[str, Any]:
        """Execute crew with monitoring"""
        self.start_time = datetime.now()

        print(f"🚀 Starting crew execution: {self.crew_id}")

        # Update dashboard
        if self.dashboard_bridge:
            self.dashboard_bridge.update_agent_status(
                self.crew_id,
                {
                    "name": "Crew Coordinator",
                    "status": "processing",
                    "current_task": "Coordinating crew execution",
                },
            )

        results = []
        agent_performances = []

        try:
            # Execute tasks sequentially (for now)
            for i, task in enumerate(self.tasks):
                print(
                    f"📋 Executing task {i + 1}/{len(self.tasks)}: {task.description[:50]}..."
                )

                # Find appropriate agent for task
                agent = self._select_agent_for_task(task)

                # Execute task
                result = agent.agent.execute(task)
                results.append(result)

                # Collect performance data
                agent_performances.append(agent.get_performance_summary())

                # Update dashboard
                if self.dashboard_bridge:
                    self.dashboard_bridge.update_agent_status(
                        self.crew_id,
                        {
                            "name": "Crew Coordinator",
                            "status": "processing",
                            "current_task": f"Completed task {i + 1}/{len(self.tasks)}",
                        },
                    )

            self.end_time = datetime.now()

            # Final dashboard update
            if self.dashboard_bridge:
                self.dashboard_bridge.update_agent_status(
                    self.crew_id,
                    {
                        "name": "Crew Coordinator",
                        "status": "completed",
                        "current_task": "All tasks completed",
                    },
                )

            print(f"✅ Crew execution completed: {self.crew_id}")

            return {
                "crew_id": self.crew_id,
                "results": results,
                "agent_performances": agent_performances,
                "execution_time": (self.end_time - self.start_time).total_seconds(),
                "success": True,
            }

        except Exception as e:
            self.end_time = datetime.now()

            # Error dashboard update
            if self.dashboard_bridge:
                self.dashboard_bridge.update_agent_status(
                    self.crew_id,
                    {
                        "name": "Crew Coordinator",
                        "status": "error",
                        "current_task": f"Error: {str(e)}",
                    },
                )

            print(f"❌ Crew execution failed: {self.crew_id} - {e}")

            return {
                "crew_id": self.crew_id,
                "error": str(e),
                "execution_time": (self.end_time - self.start_time).total_seconds(),
                "success": False,
            }

    def _select_agent_for_task(self, task: Task) -> MonitoredAgent:
        """Select appropriate agent for task"""
        # Simple selection - can be enhanced with more sophisticated logic
        # For now, just return the first available agent
        return self.agents[0]

    def get_crew_summary(self) -> Dict[str, Any]:
        """Get crew performance summary"""
        total_tasks = len(self.tasks)
        total_agents = len(self.agents)

        # Calculate crew metrics
        total_execution_time = (
            (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        )

        agent_summaries = [agent.get_performance_summary() for agent in self.agents]
        total_agent_tasks = sum(summary["total_tasks"] for summary in agent_summaries)
        total_agent_success = sum(
            summary["tasks_completed"] for summary in agent_summaries
        )

        crew_success_rate = (
            (total_agent_success / total_agent_tasks * 100)
            if total_agent_tasks > 0
            else 0
        )

        return {
            "crew_id": self.crew_id,
            "total_tasks": total_tasks,
            "total_agents": total_agents,
            "total_execution_time": total_execution_time,
            "crew_success_rate": crew_success_rate,
            "agent_summaries": agent_summaries,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }


# Convenience functions
def create_monitored_agent(
    agent: Agent,
    memory_manager: QdrantMemoryManager,
    dashboard_bridge: Optional[CrewAIDashboardBridge] = None,
) -> MonitoredAgent:
    """Create a monitored agent"""
    return MonitoredAgent(agent, memory_manager, dashboard_bridge)


def create_monitored_crew(
    agents: List[MonitoredAgent],
    tasks: List[Task],
    memory_manager: QdrantMemoryManager,
    dashboard_bridge: Optional[CrewAIDashboardBridge] = None,
) -> MonitoredCrew:
    """Create a monitored crew"""
    return MonitoredCrew(agents, tasks, memory_manager, dashboard_bridge)
