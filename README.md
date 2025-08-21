# 🚀 Reusable Coding Framework

A powerful, multi-agent coding framework built on **CrewAI** with enhanced **Qdrant** memory management. This framework enables collaborative AI agents to work together on coding projects with persistent memory, pattern recognition, and intelligent workflow orchestration.

## 🎯 Key Features

- **🤖 Multi-Agent Collaboration**: Specialized agents working together (Manager, Coder, Reviewer, Tester, Documenter)
- **🧠 Advanced Memory Management**: Vector-based memory with 8 specialized memory types
- **🔧 Customizable Tools**: MCP integration for external tools and script execution
- **📊 Real-time Dashboard**: Visual management interface for monitoring and control
- **🔄 Reusable Patterns**: Code patterns and knowledge persistence across sessions
- **⚡ High Performance**: Optimized Qdrant integration with fast embeddings

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CrewAI Core   │    │  Qdrant Memory  │    │  Custom Agents  │
│                 │    │                 │    │                 │
│ • Agents        │◄──►│ • Entity Memory │◄──►│ • Manager       │
│ • Tasks         │    │ • Short-term    │    │ • Coder         │
│ • Crews         │    │ • Long-term     │    │ • Reviewer      │
│ • Tools         │    │ • Code Snippets │    │ • Tester        │
└─────────────────┘    │ • Debug History │    │ • Documenter    │
                       │ • Project Context│    └─────────────────┘
                       │ • Communication │
                       │ • Workflow Patterns│
                       └─────────────────┘
```

## 🧠 Memory Types

### 1. **Entity Memory**
- People, tools, libraries, and concepts
- Relationship mapping and entity tracking

### 2. **Short-Term Memory**
- Recent interactions and session context
- Current task state and decisions

### 3. **Long-Term Memory**
- Persistent knowledge and learning
- Cross-session knowledge retention

### 4. **Code Snippets Memory**
- Reusable code patterns and solutions
- Language-specific code templates

### 5. **Debugging History Memory**
- Error patterns and their solutions
- Learning from past debugging sessions

### 6. **Project Context Memory**
- Project-specific information and constraints
- Requirements and configuration details

### 7. **Agent Communication Memory**
- Inter-agent message history
- Collaboration patterns and workflows

### 8. **Workflow Patterns Memory**
- Successful task execution sequences
- Optimized workflow templates

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/reusable-coding-framework.git
cd reusable-coding-framework

# Install dependencies
pip install -r requirements.txt

# Install the framework
pip install -e .
```

### 2. Setup Environment

```bash
# Create .env file
cp .env.example .env

# Configure your environment variables
OPENAI_API_KEY=your_openai_api_key

# Qdrant Cloud SaaS (recommended) - pre-configured
# No additional setup needed for cloud deployment

# OR for local development:
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### 3. Test Configuration

```bash
# Test cloud configuration
python test_qdrant_cloud.py

# OR start local Qdrant (if using local deployment)
docker run -p 6333:6333 qdrant/qdrant
```

### 4. Basic Usage

```python
from src.memory.crewai_integration import (
    EnhancedEntityMemory,
    EnhancedShortTermMemory,
    CodeSnippetsMemory
)
from crewai import Crew, Agent, Task

# Initialize memory systems
entity_memory = EnhancedEntityMemory()
short_term_memory = EnhancedShortTermMemory()
code_memory = CodeSnippetsMemory()

# Create agents with memory
manager = Agent(
    role="Project Manager",
    goal="Orchestrate successful code development",
    backstory="Expert at managing coding teams",
    memory=entity_memory
)

coder = Agent(
    role="Senior Developer",
    goal="Write high-quality, maintainable code",
    backstory="Experienced full-stack developer",
    memory=short_term_memory
)

# Create tasks
analyze_task = Task(
    description="Analyze project requirements and create task breakdown",
    agent=manager
)

code_task = Task(
    description="Implement the required functionality",
    agent=coder
)

# Create and run crew
crew = Crew(
    agents=[manager, coder],
    tasks=[analyze_task, code_task],
    memory=True,
    entity_memory=entity_memory,
    short_term_memory=short_term_memory
)

result = crew.run()
```

## 📊 Dashboard

The framework includes a real-time dashboard for monitoring agent activities, memory usage, and project progress.

```bash
# Start the dashboard
python src/dashboard/app.py
```

Dashboard features:
- **Agent Status Panel**: Live status of all agents
- **Memory Explorer**: Browse and search memory collections
- **Task Manager**: Create and monitor tasks
- **Code Quality Monitor**: Real-time quality metrics
- **Communication Logger**: Inter-agent message history
- **Performance Dashboard**: Execution statistics

## 🔧 Customization

### Custom Tools

```python
from crewai import BaseTool

class CustomCodingTool(BaseTool):
    name = "code_executor"
    description = "Execute code and return results"
    
    def _run(self, code: str) -> str:
        # Execute code safely
        return execute_code_safely(code)
```

### Custom Memory Types

```python
from src.memory.qdrant_storage import QdrantMemoryStorage

class CustomMemory(QdrantMemoryStorage):
    def __init__(self):
        super().__init__("custom_memory")
    
    def custom_method(self, data):
        # Custom memory operations
        return self.save(data, {"type": "custom"})
```

### Custom Agents

```python
from crewai import Agent
from src.memory.crewai_integration import EnhancedEntityMemory

class CustomAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Custom Role",
            goal="Custom Goal",
            backstory="Custom Backstory",
            memory=EnhancedEntityMemory()
        )
    
    def custom_method(self):
        # Custom agent behavior
        pass
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_memory.py::test_qdrant_storage
```

## 📈 Performance Optimization

### Memory Optimization
- **Batch Operations**: Group memory operations for better performance
- **Caching**: Implement caching for frequently accessed data
- **Indexing**: Optimize Qdrant collections with proper indexing

### Agent Optimization
- **Parallel Execution**: Run agents in parallel when possible
- **Resource Management**: Monitor and optimize resource usage
- **Error Handling**: Implement robust error handling and recovery

## 🔒 Security

- **API Key Management**: Secure storage of API keys
- **Code Execution Safety**: Sandboxed code execution
- **Memory Access Control**: Controlled access to memory systems
- **Input Validation**: Validate all inputs and outputs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI**: For the excellent multi-agent framework
- **Qdrant**: For the powerful vector database
- **OpenAI**: For the embedding and language models
- **FastEmbed**: For fast and efficient embeddings

## 📞 Support

- **Documentation**: [Framework Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/reusable-coding-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/reusable-coding-framework/discussions)

## 🚀 Roadmap

- [ ] **Enhanced Dashboard**: Advanced visualization and control features
- [ ] **Multi-Modal Support**: Image and audio processing capabilities
- [ ] **Distributed Agents**: Support for distributed agent deployment
- [ ] **Advanced Analytics**: Deep insights into agent performance and patterns
- [ ] **Plugin System**: Extensible plugin architecture for custom integrations
- [ ] **Cloud Deployment**: Easy deployment to cloud platforms

---

**Built with ❤️ for the AI development community**
