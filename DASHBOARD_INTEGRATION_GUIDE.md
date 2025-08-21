# 🚀 Dashboard Integration Guide
## CrewAI + Qdrant + Dashboard Framework

This guide explains how to integrate your existing dashboard with our CrewAI + Qdrant framework for real-time monitoring and metrics collection.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Setup Instructions](#setup-instructions)
4. [Integration Steps](#integration-steps)
5. [Usage Examples](#usage-examples)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Your dashboard system provides a comprehensive monitoring interface for multi-agent systems. Our framework integration adds:

- **Real-time Metrics Collection**: Automatic collection of agent performance metrics
- **Qdrant Memory Integration**: Vector-based memory storage for patterns and knowledge
- **Dashboard Bridge**: Seamless connection between framework and dashboard
- **Enhanced Agents**: Monitored agents with performance tracking
- **Memory Analytics**: Insights into agent behavior and patterns

---

## 🏗️ Architecture

```mermaid
graph TD
    A[CrewAI Agents] --> B[Monitored Agents]
    B --> C[Metrics Collector]
    C --> D[Qdrant Memory]
    C --> E[Dashboard Bridge]
    E --> F[WebSocket Server]
    F --> G[Dashboard UI]
    D --> H[Memory Analytics]
    H --> G
```

### Components:

1. **Monitored Agents**: Enhanced CrewAI agents with performance tracking
2. **Metrics Collector**: Collects and processes agent metrics
3. **Dashboard Bridge**: Connects framework to dashboard WebSocket
4. **Qdrant Memory**: Vector storage for patterns and knowledge
5. **WebSocket Server**: Real-time data streaming to dashboard

---

## ⚙️ Setup Instructions

### Prerequisites

1. **Python Environment**:
   ```bash
   python 3.8+
   pip install -r requirements.txt
   ```

2. **Qdrant Database** (Cloud SaaS Recommended):
   ```bash
   # Cloud SaaS (recommended) - no local setup needed
   # Use provided cloud credentials:
   # URL: https://55182465-43a7-4ee6-9617-3dd69263e4f7.eu-central-1-0.aws.cloud.qdrant.io:6333
   # API Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzYzNTgxMDU4fQ.D2nNPup_5bg2WPFAEsDYYi6xMa7_gPj8-X3d-Rd9Rms
   
   # OR for local development:
   docker run -d -p 6333:6333 qdrant/qdrant
   ```

3. **Dashboard Services**:
   ```bash
   cd dashboard
   ./start-all.sh
   ```

### Framework Installation

1. **Clone and Setup**:
   ```bash
   git clone <your-repo>
   cd <your-repo>
   pip install -e .
   ```

2. **Environment Variables**:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   
   # For Cloud SaaS (recommended):
   export QDRANT_URL="https://55182465-43a7-4ee6-9617-3dd69263e4f7.eu-central-1-0.aws.cloud.qdrant.io:6333"
   export QDRANT_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzYzNTgxMDU4fQ.D2nNPup_5bg2WPFAEsDYYi6xMa7_gPj8-X3d-Rd9Rms"
   
   # OR for local development:
   export QDRANT_HOST="localhost"
   export QDRANT_PORT="6333"
   ```

3. **Verify Setup**:
   ```bash
   python examples/complete_framework_example.py
   ```

---

## 🔗 Integration Steps

### Step 1: Initialize Framework Components

```python
from memory.qdrant_storage import QdrantMemoryManager
from dashboard.framework_bridge import create_dashboard_bridge
from agents.monitored_agent import create_monitored_agent

# Initialize memory manager with cloud configuration
memory_manager = QdrantMemoryManager(use_cloud=True)

# Create dashboard bridge
dashboard_bridge = create_dashboard_bridge(memory_manager)

# Start monitoring
await dashboard_bridge.start_monitoring()
```

### Step 2: Create Monitored Agents

```python
from crewai import Agent

# Create standard CrewAI agent
researcher = Agent(
    role="Research Analyst",
    goal="Research and analyze information",
    backstory="Expert researcher with deep knowledge...",
    verbose=True
)

# Wrap with monitoring
monitored_researcher = create_monitored_agent(
    researcher, 
    memory_manager, 
    dashboard_bridge
)
```

### Step 3: Execute with Monitoring

```python
from agents.monitored_agent import create_monitored_crew

# Create monitored crew
crew = create_monitored_crew(
    agents=[monitored_researcher],
    tasks=[research_task],
    memory_manager=memory_manager,
    dashboard_bridge=dashboard_bridge
)

# Execute with real-time monitoring
result = await crew.execute()
```

---

## 📊 Usage Examples

### Example 1: Basic Integration

```python
import asyncio
from crewai import Agent, Task
from memory.qdrant_storage import QdrantMemoryManager
from dashboard.framework_bridge import create_dashboard_bridge
from agents.monitored_agent import create_monitored_agent, create_monitored_crew

async def basic_example():
    # Setup
    memory_manager = QdrantMemoryManager()
    dashboard_bridge = create_dashboard_bridge(memory_manager)
    await dashboard_bridge.start_monitoring()
    
    # Create agent
    agent = Agent(role="Analyst", goal="Analyze data")
    monitored_agent = create_monitored_agent(agent, memory_manager, dashboard_bridge)
    
    # Create task
    task = Task(description="Analyze market trends", agent=agent)
    
    # Execute
    crew = create_monitored_crew([monitored_agent], [task], memory_manager, dashboard_bridge)
    result = await crew.execute()
    
    # Cleanup
    await dashboard_bridge.stop_monitoring()
    
    return result

# Run example
asyncio.run(basic_example())
```

### Example 2: Multi-Agent Workflow

```python
async def multi_agent_example():
    # Setup
    memory_manager = QdrantMemoryManager()
    dashboard_bridge = create_dashboard_bridge(memory_manager)
    await dashboard_bridge.start_monitoring()
    
    # Create multiple agents
    agents = [
        Agent(role="Researcher", goal="Research topics"),
        Agent(role="Writer", goal="Write content"),
        Agent(role="Reviewer", goal="Review quality")
    ]
    
    # Wrap with monitoring
    monitored_agents = [
        create_monitored_agent(agent, memory_manager, dashboard_bridge)
        for agent in agents
    ]
    
    # Create tasks
    tasks = [
        Task(description="Research AI trends", agent=agents[0]),
        Task(description="Write article", agent=agents[1]),
        Task(description="Review article", agent=agents[2])
    ]
    
    # Execute crew
    crew = create_monitored_crew(monitored_agents, tasks, memory_manager, dashboard_bridge)
    result = await crew.execute()
    
    # Get performance summary
    summary = crew.get_crew_summary()
    print(f"Crew success rate: {summary['crew_success_rate']:.1f}%")
    
    await dashboard_bridge.stop_monitoring()
    return result
```

### Example 3: Memory Analytics

```python
def memory_analytics_example():
    memory_manager = QdrantMemoryManager()
    
    # Get memory statistics
    stats = memory_manager.get_all_stats()
    print("Memory Collections:")
    for collection, data in stats.items():
        print(f"  {collection}: {data.get('points_count', 0)} records")
    
    # Search for patterns
    patterns = memory_manager.retrieve_from_memory(
        "workflow_patterns", 
        "successful task execution", 
        limit=5
    )
    
    print(f"Found {len(patterns)} successful patterns")
    
    # Search for errors
    errors = memory_manager.retrieve_from_memory(
        "debugging_history", 
        "error patterns", 
        limit=5
    )
    
    print(f"Found {len(errors)} error patterns")
```

---

## 🎨 Customization

### Custom Metrics Collection

```python
class CustomMetricsCollector:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
    
    def collect_custom_metrics(self, agent_id: str, data: dict):
        """Collect custom metrics for specific agent"""
        metrics_data = {
            "agent_id": agent_id,
            "custom_metric": data.get("custom_value"),
            "timestamp": datetime.now().isoformat()
        }
        
        # Store in custom collection
        self.memory_manager.save_to_memory(
            "custom_metrics", 
            metrics_data, 
            {"metric_type": "custom"}
        )
```

### Custom Dashboard Updates

```python
class CustomDashboardBridge:
    def __init__(self, dashboard_bridge):
        self.bridge = dashboard_bridge
    
    async def send_custom_update(self, data: dict):
        """Send custom data to dashboard"""
        custom_data = {
            "type": "custom_update",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Send via WebSocket
        if self.bridge.websocket_server:
            await self.bridge.websocket_server.send(json.dumps(custom_data))
```

### Custom Memory Types

```python
def create_custom_memory_type(memory_manager, collection_name: str):
    """Create custom memory collection"""
    storage = memory_manager.get_storage(collection_name)
    
    def save_custom_data(data: dict, metadata: dict = None):
        return storage.save(data, metadata)
    
    def retrieve_custom_data(query: str, limit: int = 5):
        return storage.retrieve(query, limit)
    
    return {
        "save": save_custom_data,
        "retrieve": retrieve_custom_data,
        "storage": storage
    }

# Usage
custom_memory = create_custom_memory_type(memory_manager, "custom_collection")
custom_memory["save"]({"key": "value"}, {"type": "custom"})
```

---

## 🔧 Troubleshooting

### Common Issues

1. **Dashboard Not Connecting**:
   ```bash
   # Check WebSocket server
   curl http://localhost:8765
   
   # Check dashboard
   curl http://localhost:8080
   ```

2. **Qdrant Connection Issues**:
   ```bash
   # Check Qdrant status
   curl http://localhost:6333/health
   
   # Restart Qdrant
   docker restart qdrant
   ```

3. **Memory Collection Errors**:
   ```python
   # Check collection status
   stats = memory_manager.get_all_stats()
   print(stats)
   
   # Reset collections if needed
   memory_manager.reset_all()
   ```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug info
dashboard_bridge = create_dashboard_bridge(memory_manager)
await dashboard_bridge.start_monitoring()
```

### Performance Monitoring

```python
# Monitor memory usage
import psutil
process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")

# Monitor Qdrant performance
stats = memory_manager.get_all_stats()
for collection, data in stats.items():
    print(f"{collection}: {data.get('points_count', 0)} points")
```

---

## 📈 Advanced Features

### Real-time Analytics

```python
async def real_time_analytics():
    dashboard_bridge = create_dashboard_bridge(memory_manager)
    await dashboard_bridge.start_monitoring()
    
    # Get real-time metrics
    while True:
        metrics = dashboard_bridge.get_dashboard_data()
        
        # Analyze patterns
        system_metrics = metrics["system"]
        print(f"TCR: {system_metrics['task_completion_rate']:.1f}%")
        print(f"Velocity: {system_metrics['system_velocity']:.1f} tasks/min")
        
        await asyncio.sleep(1)
```

### Pattern Recognition

```python
def analyze_patterns():
    # Find successful patterns
    successful_patterns = memory_manager.retrieve_from_memory(
        "workflow_patterns",
        "successful execution",
        limit=10
    )
    
    # Analyze patterns
    for pattern in successful_patterns:
        execution_time = pattern.get("execution_time", 0)
        if execution_time < 5.0:  # Fast execution
            print(f"Fast pattern: {pattern.get('task_description', 'N/A')}")
```

### Predictive Analytics

```python
def predict_performance():
    # Get historical data
    history = memory_manager.retrieve_from_memory(
        "agent_communication",
        "performance history",
        limit=100
    )
    
    # Simple prediction based on history
    success_rates = [h.get("success_rate", 0) for h in history]
    avg_success_rate = sum(success_rates) / len(success_rates) if success_rates else 0
    
    print(f"Predicted success rate: {avg_success_rate:.1f}%")
```

---

## 🎯 Best Practices

1. **Memory Management**:
   - Regularly clean old data
   - Use appropriate collection types
   - Monitor memory usage

2. **Dashboard Updates**:
   - Send updates at appropriate intervals
   - Handle connection failures gracefully
   - Use efficient data formats

3. **Agent Monitoring**:
   - Track meaningful metrics
   - Store patterns for reuse
   - Monitor error rates

4. **Performance Optimization**:
   - Use async operations
   - Batch memory operations
   - Optimize query patterns

---

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Dashboard Documentation](./dashboard/README.md)
- [Framework Architecture](./FRAMEWORK_ARCHITECTURE.md)

---

## 🤝 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the examples
3. Check the dashboard logs
4. Open an issue in the repository

---

**Happy Monitoring! 🚀**
