"""
Framework-Dashboard Bridge
Connects our CrewAI + Qdrant framework with the existing dashboard
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

from ..memory.qdrant_storage import QdrantMemoryManager
from ..memory.crewai_integration import CrewAIQdrantStorage


@dataclass
class AgentMetrics:
    """Agent performance metrics"""

    agent_id: str
    agent_name: str
    status: str  # 'active', 'idle', 'error', 'processing'
    tasks_completed: int
    tasks_failed: int
    current_task: Optional[str]
    cpu_usage: float
    memory_usage: float
    response_time: float
    last_activity: datetime
    health_score: float  # 0-100


@dataclass
class SystemMetrics:
    """System-wide metrics"""

    total_agents: int
    active_agents: int
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    system_velocity: float  # tasks per minute
    task_completion_rate: float  # percentage
    coordination_score: float  # 0-5
    collective_intelligence: float  # emergence coefficient
    memory_usage: Dict[str, int]  # per collection
    timestamp: datetime


class MetricsCollector:
    """Collects metrics from CrewAI framework"""

    def __init__(self, memory_manager: QdrantMemoryManager):
        self.memory_manager = memory_manager
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.system_metrics_history: List[SystemMetrics] = []

    def update_agent_metrics(self, agent_id: str, metrics: Dict[str, Any]):
        """Update metrics for specific agent"""
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentMetrics(
                agent_id=agent_id,
                agent_name=metrics.get("name", agent_id),
                status="active",
                tasks_completed=0,
                tasks_failed=0,
                current_task=None,
                cpu_usage=0.0,
                memory_usage=0.0,
                response_time=0.0,
                last_activity=datetime.now(),
                health_score=100.0,
            )

        # Update existing metrics
        agent = self.agent_metrics[agent_id]
        agent.status = metrics.get("status", agent.status)
        agent.tasks_completed = metrics.get("tasks_completed", agent.tasks_completed)
        agent.tasks_failed = metrics.get("tasks_failed", agent.tasks_failed)
        agent.current_task = metrics.get("current_task", agent.current_task)
        agent.cpu_usage = metrics.get("cpu_usage", agent.cpu_usage)
        agent.memory_usage = metrics.get("memory_usage", agent.memory_usage)
        agent.response_time = metrics.get("response_time", agent.response_time)
        agent.last_activity = datetime.now()

        # Calculate health score
        agent.health_score = self._calculate_health_score(agent)

    def get_system_metrics(self) -> SystemMetrics:
        """Calculate current system metrics"""
        total_agents = len(self.agent_metrics)
        active_agents = sum(
            1 for agent in self.agent_metrics.values() if agent.status == "active"
        )

        total_tasks = sum(
            agent.tasks_completed + agent.tasks_failed
            for agent in self.agent_metrics.values()
        )
        completed_tasks = sum(
            agent.tasks_completed for agent in self.agent_metrics.values()
        )
        failed_tasks = sum(agent.tasks_failed for agent in self.agent_metrics.values())

        # Calculate velocity (tasks per minute)
        system_velocity = self._calculate_velocity()

        # Calculate TCR
        task_completion_rate = (
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        )

        # Calculate coordination score
        coordination_score = self._calculate_coordination_score()

        # Calculate collective intelligence
        collective_intelligence = self._calculate_collective_intelligence()

        # Get memory usage
        memory_usage = self._get_memory_usage()

        metrics = SystemMetrics(
            total_agents=total_agents,
            active_agents=active_agents,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            failed_tasks=failed_tasks,
            system_velocity=system_velocity,
            task_completion_rate=task_completion_rate,
            coordination_score=coordination_score,
            collective_intelligence=collective_intelligence,
            memory_usage=memory_usage,
            timestamp=datetime.now(),
        )

        # Store in history
        self.system_metrics_history.append(metrics)

        # Keep only last 1000 entries
        if len(self.system_metrics_history) > 1000:
            self.system_metrics_history = self.system_metrics_history[-1000:]

        return metrics

    def _calculate_health_score(self, agent: AgentMetrics) -> float:
        """Calculate agent health score (0-100)"""
        score = 100.0

        # Penalize for failed tasks
        if agent.tasks_completed + agent.tasks_failed > 0:
            failure_rate = agent.tasks_failed / (
                agent.tasks_completed + agent.tasks_failed
            )
            score -= failure_rate * 30

        # Penalize for high resource usage
        if agent.cpu_usage > 80:
            score -= (agent.cpu_usage - 80) * 0.5

        if agent.memory_usage > 80:
            score -= (agent.memory_usage - 80) * 0.5

        # Penalize for slow response time
        if agent.response_time > 5.0:  # 5 seconds
            score -= (agent.response_time - 5.0) * 5

        # Penalize for inactivity
        time_since_activity = (datetime.now() - agent.last_activity).total_seconds()
        if time_since_activity > 300:  # 5 minutes
            score -= min(time_since_activity / 60, 20)  # Max 20 point penalty

        return max(0.0, score)

    def _calculate_velocity(self) -> float:
        """Calculate system velocity (tasks per minute)"""
        if len(self.system_metrics_history) < 2:
            return 0.0

        # Get tasks completed in last minute
        one_minute_ago = datetime.now().timestamp() - 60
        recent_metrics = [
            m
            for m in self.system_metrics_history
            if m.timestamp.timestamp() > one_minute_ago
        ]

        if len(recent_metrics) < 2:
            return 0.0

        first_metric = recent_metrics[0]
        last_metric = recent_metrics[-1]

        tasks_diff = last_metric.completed_tasks - first_metric.completed_tasks
        time_diff = (
            last_metric.timestamp - first_metric.timestamp
        ).total_seconds() / 60

        return tasks_diff / time_diff if time_diff > 0 else 0.0

    def _calculate_coordination_score(self) -> float:
        """Calculate coordination score (0-5)"""
        if not self.agent_metrics:
            return 0.0

        # Base score on agent communication patterns
        communication_score = 0.0

        # Check for task handoffs
        task_handoffs = self._count_task_handoffs()
        communication_score += min(task_handoffs / 10, 2.0)  # Max 2 points

        # Check for parallel processing
        parallel_tasks = sum(
            1 for agent in self.agent_metrics.values() if agent.current_task is not None
        )
        communication_score += min(
            parallel_tasks / len(self.agent_metrics), 2.0
        )  # Max 2 points

        # Check for error recovery
        error_recovery = self._check_error_recovery()
        communication_score += error_recovery  # Max 1 point

        return min(5.0, communication_score)

    def _calculate_collective_intelligence(self) -> float:
        """Calculate collective intelligence coefficient"""
        if not self.agent_metrics:
            return 1.0

        # Calculate individual performance
        individual_performance = sum(
            agent.health_score for agent in self.agent_metrics.values()
        )
        individual_performance /= len(self.agent_metrics)

        # Calculate collective performance
        system_metrics = self.get_system_metrics()
        collective_performance = system_metrics.task_completion_rate

        # Calculate emergence coefficient
        if individual_performance > 0:
            emergence = collective_performance / individual_performance
            return min(2.0, max(0.5, emergence))

        return 1.0

    def _get_memory_usage(self) -> Dict[str, int]:
        """Get memory usage for all collections"""
        try:
            stats = self.memory_manager.get_all_stats()
            return {name: stats.get("points_count", 0) for name, stats in stats.items()}
        except Exception as e:
            print(f"Error getting memory usage: {e}")
            return {}

    def _count_task_handoffs(self) -> int:
        """Count task handoffs between agents"""
        # This would analyze communication patterns
        # For now, return a simulated value
        return len(self.agent_metrics) * 2

    def _check_error_recovery(self) -> float:
        """Check error recovery patterns"""
        # This would analyze error patterns and recovery
        # For now, return a simulated value
        return 0.8


class CrewAIDashboardBridge:
    """Main bridge between CrewAI framework and dashboard"""

    def __init__(self, memory_manager: QdrantMemoryManager):
        self.memory_manager = memory_manager
        self.metrics_collector = MetricsCollector(memory_manager)
        self.websocket_server = None
        self.monitoring_task = None

    async def start_monitoring(self, websocket_url: str = "ws://localhost:8765"):
        """Start real-time monitoring"""
        print("🚀 Starting CrewAI Dashboard Bridge...")

        # Start metrics collection
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())

        # Connect to existing WebSocket server
        await self._connect_to_dashboard(websocket_url)

        print("✅ Dashboard bridge started successfully")

    async def _monitoring_loop(self):
        """Continuous monitoring loop"""
        while True:
            try:
                # Update system metrics
                system_metrics = self.metrics_collector.get_system_metrics()

                # Send to dashboard
                await self._send_metrics_to_dashboard(system_metrics)

                # Wait 100ms
                await asyncio.sleep(0.1)

            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                await asyncio.sleep(1)

    async def _connect_to_dashboard(self, websocket_url: str):
        """Connect to existing dashboard WebSocket server"""
        try:
            import websockets

            self.websocket_server = await websockets.connect(websocket_url)
            print(f"✅ Connected to dashboard at {websocket_url}")

        except Exception as e:
            print(f"⚠️  Could not connect to dashboard: {e}")
            print("Dashboard will work in simulation mode")

    async def _send_metrics_to_dashboard(self, metrics: SystemMetrics):
        """Send metrics to dashboard"""
        if not self.websocket_server:
            return

        try:
            # Convert metrics to dashboard format
            dashboard_data = {
                "type": "system_update",
                "timestamp": metrics.timestamp.isoformat(),
                "system_tcr": metrics.task_completion_rate,
                "system_velocity": metrics.system_velocity,
                "coordination_score": metrics.coordination_score,
                "collective_intelligence": metrics.collective_intelligence,
                "total_agents": metrics.total_agents,
                "active_agents": metrics.active_agents,
                "memory_usage": metrics.memory_usage,
            }

            await self.websocket_server.send(json.dumps(dashboard_data))

        except Exception as e:
            print(f"Error sending metrics to dashboard: {e}")

    def update_agent_status(self, agent_id: str, status_data: Dict[str, Any]):
        """Update agent status (called from framework)"""
        self.metrics_collector.update_agent_metrics(agent_id, status_data)

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get current dashboard data"""
        system_metrics = self.metrics_collector.get_system_metrics()

        return {
            "system": asdict(system_metrics),
            "agents": {
                agent_id: asdict(agent)
                for agent_id, agent in self.metrics_collector.agent_metrics.items()
            },
            "memory": self.metrics_collector._get_memory_usage(),
        }

    async def stop_monitoring(self):
        """Stop monitoring"""
        if self.monitoring_task:
            self.monitoring_task.cancel()

        if self.websocket_server:
            await self.websocket_server.close()

        print("🛑 Dashboard bridge stopped")


# Convenience function for framework integration
def create_dashboard_bridge(
    memory_manager: QdrantMemoryManager,
) -> CrewAIDashboardBridge:
    """Create and return dashboard bridge instance"""
    return CrewAIDashboardBridge(memory_manager)
