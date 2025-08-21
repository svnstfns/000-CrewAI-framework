#!/usr/bin/env python3
"""
Example CrewAI implementation with Dashboard monitoring
"""

from crewai import Agent, Task, Crew
import redis
import json
import time
from datetime import datetime
from typing import Dict, Any

class DashboardMonitor:
    """Simple monitoring class for CrewAI agents"""
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.agent_metrics = {}
        
    def report_task_start(self, agent_name: str, task_id: str):
        """Report when a task starts"""
        data = {
            'agent': agent_name,
            'task_id': task_id,
            'status': 'in_progress',
            'timestamp': datetime.now().isoformat()
        }
        
        # Update Redis
        self.redis_client.hset(
            f'task:{task_id}',
            mapping=data
        )
        
        # Publish event
        self.redis_client.publish(
            'dashboard:tasks',
            json.dumps(data)
        )
        
        print(f"[MONITOR] Task {task_id} started by {agent_name}")
        
    def report_task_completion(self, agent_name: str, task_id: str, 
                              success: bool, duration: float):
        """Report when a task completes"""
        data = {
            'agent': agent_name,
            'task_id': task_id,
            'status': 'done' if success else 'failed',
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }
        
        # Update task status
        self.redis_client.hset(
            f'task:{task_id}',
            mapping=data
        )
        
        # Update agent metrics
        self._update_agent_metrics(agent_name, success, duration)
        
        # Publish event
        self.redis_client.publish(
            'dashboard:tasks',
            json.dumps(data)
        )
        
        print(f"[MONITOR] Task {task_id} completed: {'✓' if success else '✗'} ({duration:.2f}s)")
        
    def _update_agent_metrics(self, agent_name: str, success: bool, duration: float):
        """Update agent performance metrics"""
        
        # Initialize metrics if needed
        if agent_name not in self.agent_metrics:
            self.agent_metrics[agent_name] = {
                'total_tasks': 0,
                'successful_tasks': 0,
                'total_duration': 0
            }
        
        # Update metrics
        metrics = self.agent_metrics[agent_name]
        metrics['total_tasks'] += 1
        if success:
            metrics['successful_tasks'] += 1
        metrics['total_duration'] += duration
        
        # Calculate TCR and average duration
        tcr = (metrics['successful_tasks'] / metrics['total_tasks']) * 100
        avg_duration = metrics['total_duration'] / metrics['total_tasks']
        
        # Report to dashboard
        dashboard_metrics = {
            'agent_id': agent_name,
            'task_completion_rate': tcr,
            'avg_task_duration': avg_duration,
            'total_tasks': metrics['total_tasks'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in Redis
        self.redis_client.hset(
            f'agent:metrics:{agent_name}',
            mapping=dashboard_metrics
        )
        
        # Publish metrics update
        self.redis_client.publish(
            'dashboard:metrics',
            json.dumps(dashboard_metrics)
        )
        
    def report_system_metrics(self):
        """Report overall system metrics"""
        
        # Calculate system-wide metrics
        total_agents = len(self.agent_metrics)
        total_tasks = sum(m['total_tasks'] for m in self.agent_metrics.values())
        total_successful = sum(m['successful_tasks'] for m in self.agent_metrics.values())
        
        system_tcr = (total_successful / total_tasks * 100) if total_tasks > 0 else 0
        
        system_metrics = {
            'total_agents': total_agents,
            'total_tasks': total_tasks,
            'system_tcr': system_tcr,
            'system_velocity': total_tasks / (time.time() / 60),  # tasks per minute
            'timestamp': datetime.now().isoformat()
        }
        
        # Store and publish
        self.redis_client.hset(
            'system:metrics',
            mapping=system_metrics
        )
        
        self.redis_client.publish(
            'dashboard:system',
            json.dumps(system_metrics)
        )
        
        print(f"[MONITOR] System: {total_agents} agents, {total_tasks} tasks, TCR: {system_tcr:.1f}%")


# Create monitoring wrapper for agents
def create_monitored_agent(name: str, role: str, goal: str, 
                          backstory: str, monitor: DashboardMonitor):
    """Create an agent with monitoring capabilities"""
    
    agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True
    )
    
    # Store original execute method
    original_execute = agent.execute
    
    # Create monitored version
    def monitored_execute(task):
        task_id = f"task_{name}_{int(time.time())}"
        monitor.report_task_start(name, task_id)
        
        start_time = time.time()
        try:
            result = original_execute(task)
            duration = time.time() - start_time
            monitor.report_task_completion(name, task_id, True, duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            monitor.report_task_completion(name, task_id, False, duration)
            raise e
    
    # Replace execute method
    agent.execute = monitored_execute
    agent.name = name  # Store agent name
    
    return agent


def main():
    """Example CrewAI setup with dashboard monitoring"""
    
    print("🚀 Starting CrewAI with Dashboard Monitoring")
    print("=" * 50)
    
    # Initialize monitor
    monitor = DashboardMonitor()
    
    # Create monitored agents
    researcher = create_monitored_agent(
        name="researcher",
        role="Senior Research Analyst",
        goal="Research and analyze information about multi-agent systems",
        backstory="""You are a senior research analyst with expertise in 
                     distributed systems and AI architectures.""",
        monitor=monitor
    )
    
    writer = create_monitored_agent(
        name="writer",
        role="Technical Writer",
        goal="Create clear and comprehensive documentation",
        backstory="""You are an experienced technical writer who specializes 
                     in making complex topics accessible.""",
        monitor=monitor
    )
    
    reviewer = create_monitored_agent(
        name="reviewer",
        role="Quality Reviewer",
        goal="Review and improve content quality",
        backstory="""You are a meticulous reviewer who ensures high quality 
                     standards in all deliverables.""",
        monitor=monitor
    )
    
    # Create tasks
    research_task = Task(
        description="""Research the following topics about multi-agent systems:
                      1. Current architectures and frameworks
                      2. Communication protocols between agents
                      3. Monitoring and observability best practices
                      Provide a comprehensive summary.""",
        agent=researcher,
        expected_output="A detailed research report on multi-agent systems"
    )
    
    writing_task = Task(
        description="""Based on the research, write a technical article about 
                      implementing multi-agent systems with proper monitoring.
                      Include code examples and best practices.""",
        agent=writer,
        expected_output="A well-structured technical article"
    )
    
    review_task = Task(
        description="""Review the article for:
                      1. Technical accuracy
                      2. Clarity and readability
                      3. Completeness
                      Provide feedback and suggestions.""",
        agent=reviewer,
        expected_output="Review feedback and improved content"
    )
    
    # Create crew
    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=[research_task, writing_task, review_task],
        verbose=True
    )
    
    print("\n📊 Dashboard Monitoring Active")
    print("Check http://localhost:8080 for real-time updates")
    print("-" * 50)
    
    # Execute crew
    try:
        print("\n🔄 Starting crew execution...")
        result = crew.kickoff()
        
        print("\n✅ Crew execution completed!")
        print("-" * 50)
        print("Result:", result[:500] if len(result) > 500 else result)
        
        # Report final system metrics
        monitor.report_system_metrics()
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        
    print("\n📈 Final Metrics:")
    print("-" * 50)
    
    # Display final metrics
    for agent_name, metrics in monitor.agent_metrics.items():
        tcr = (metrics['successful_tasks'] / metrics['total_tasks'] * 100) if metrics['total_tasks'] > 0 else 0
        print(f"{agent_name}:")
        print(f"  Tasks: {metrics['total_tasks']}")
        print(f"  Success Rate: {tcr:.1f}%")
        print(f"  Avg Duration: {metrics['total_duration']/metrics['total_tasks']:.2f}s")


if __name__ == "__main__":
    # Check Redis connection
    try:
        r = redis.Redis(host='localhost', port=6379)
        r.ping()
        print("✅ Redis connected")
    except:
        print("❌ Redis not available. Please start Redis first:")
        print("   docker run -d -p 6379:6379 redis:7-alpine")
        exit(1)
    
    main()
