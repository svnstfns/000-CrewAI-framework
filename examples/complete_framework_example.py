#!/usr/bin/env python3
"""
Complete Framework Example
Demonstrates the entire CrewAI + Qdrant + Dashboard framework
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from crewai import Agent, Task
from memory.qdrant_storage import QdrantMemoryManager
from dashboard.framework_bridge import create_dashboard_bridge
from agents.monitored_agent import create_monitored_agent, create_monitored_crew


async def main():
    """Main example function"""
    print("🚀 CrewAI + Qdrant + Dashboard Framework Example")
    print("=" * 60)

    # Initialize memory manager with cloud configuration
    print("\n📦 Initializing Qdrant Memory Manager (Cloud SaaS)...")
    memory_manager = QdrantMemoryManager(use_cloud=True)

    # Initialize dashboard bridge
    print("📊 Initializing Dashboard Bridge...")
    dashboard_bridge = create_dashboard_bridge(memory_manager)

    # Start dashboard monitoring
    print("🔗 Starting Dashboard Monitoring...")
    await dashboard_bridge.start_monitoring()

    # Create CrewAI agents
    print("\n🤖 Creating CrewAI Agents...")

    researcher = Agent(
        role="Senior Research Analyst",
        goal="Research and analyze information about multi-agent systems and AI frameworks",
        backstory="""You are a senior research analyst with expertise in 
                     distributed systems, AI architectures, and emerging technologies.
                     You have a deep understanding of multi-agent systems and their applications.""",
        verbose=True,
        allow_delegation=False,
    )

    writer = Agent(
        role="Technical Writer",
        goal="Create clear, comprehensive, and engaging technical documentation",
        backstory="""You are an experienced technical writer who specializes 
                     in making complex topics accessible to different audiences.
                     You excel at creating documentation that is both informative and engaging.""",
        verbose=True,
        allow_delegation=False,
    )

    reviewer = Agent(
        role="Quality Reviewer",
        goal="Review and improve content quality, accuracy, and completeness",
        backstory="""You are a meticulous reviewer who ensures high quality 
                     standards in all deliverables. You have a keen eye for detail
                     and can identify areas for improvement in technical content.""",
        verbose=True,
        allow_delegation=False,
    )

    # Create monitored agents
    print("🔍 Wrapping agents with monitoring...")
    monitored_researcher = create_monitored_agent(
        researcher, memory_manager, dashboard_bridge
    )
    monitored_writer = create_monitored_agent(writer, memory_manager, dashboard_bridge)
    monitored_reviewer = create_monitored_agent(
        reviewer, memory_manager, dashboard_bridge
    )

    # Create tasks
    print("\n📋 Creating Tasks...")

    research_task = Task(
        description="""Research the following topics about multi-agent systems:
                      1. Current architectures and frameworks (CrewAI, LangGraph, etc.)
                      2. Communication protocols between agents
                      3. Memory management and persistence strategies
                      4. Monitoring and observability best practices
                      5. Performance optimization techniques
                      
                      Provide a comprehensive analysis with:
                      - Key findings and insights
                      - Comparison of different approaches
                      - Recommendations for implementation
                      - Real-world use cases and examples""",
        agent=researcher,
        expected_output="A detailed research report on multi-agent systems with actionable insights",
    )

    writing_task = Task(
        description="""Based on the research findings, write a comprehensive technical article about 
                      implementing multi-agent systems with proper monitoring and memory management.
                      
                      The article should include:
                      - Introduction to multi-agent systems
                      - Architecture patterns and best practices
                      - Code examples and implementation details
                      - Monitoring and observability strategies
                      - Memory management approaches
                      - Performance considerations
                      - Real-world case studies
                      
                      Make it accessible to both technical and non-technical audiences.""",
        agent=writer,
        expected_output="A well-structured technical article with code examples and best practices",
    )

    review_task = Task(
        description="""Review the technical article for:
                      1. Technical accuracy and completeness
                      2. Clarity and readability
                      3. Code quality and best practices
                      4. Logical flow and structure
                      5. Audience appropriateness
                      6. Actionable insights and recommendations
                      
                      Provide detailed feedback including:
                      - Strengths and areas for improvement
                      - Specific suggestions for enhancement
                      - Technical corrections if needed
                      - Overall assessment and recommendations""",
        agent=reviewer,
        expected_output="Comprehensive review feedback with specific improvement suggestions",
    )

    # Create monitored crew
    print("👥 Creating Monitored Crew...")
    monitored_agents = [monitored_researcher, monitored_writer, monitored_reviewer]
    tasks = [research_task, writing_task, review_task]

    crew = create_monitored_crew(
        monitored_agents, tasks, memory_manager, dashboard_bridge
    )

    # Execute crew
    print("\n🚀 Executing Crew...")
    print("📊 Dashboard available at: http://localhost:8080")
    print("🔌 WebSocket server: ws://localhost:8765")
    print("-" * 60)

    try:
        result = await crew.execute()

        if result["success"]:
            print("\n✅ Crew execution completed successfully!")
            print(f"⏱️  Total execution time: {result['execution_time']:.2f} seconds")

            # Display results
            print("\n📄 Results:")
            print("-" * 40)
            for i, task_result in enumerate(result["results"]):
                print(f"Task {i + 1}: {str(task_result)[:100]}...")

            # Display agent performances
            print("\n🤖 Agent Performance Summary:")
            print("-" * 40)
            for performance in result["agent_performances"]:
                print(f"Agent: {performance['role']}")
                print(f"  Success Rate: {performance['success_rate']:.1f}%")
                print(
                    f"  Tasks: {performance['total_tasks']} (✓{performance['tasks_completed']} ✗{performance['tasks_failed']})"
                )
                print(
                    f"  Avg Response Time: {performance['average_response_time']:.2f}s"
                )
                print()

            # Get crew summary
            crew_summary = crew.get_crew_summary()
            print(f"👥 Crew Success Rate: {crew_summary['crew_success_rate']:.1f}%")

        else:
            print(f"\n❌ Crew execution failed: {result['error']}")

    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # Stop dashboard monitoring
        print("\n🛑 Stopping Dashboard Monitoring...")
        await dashboard_bridge.stop_monitoring()

        # Display memory statistics
        print("\n📊 Memory Statistics:")
        print("-" * 40)
        stats = memory_manager.get_all_stats()
        for collection_name, collection_stats in stats.items():
            print(
                f"{collection_name}: {collection_stats.get('points_count', 0)} records"
            )

        print("\n🎉 Framework example completed!")
        print("=" * 60)


def setup_environment():
    """Setup environment variables"""
    # Set OpenAI API key if not already set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False

    return True


if __name__ == "__main__":
    print("🔧 Setting up environment...")
    if not setup_environment():
        print("❌ Environment setup failed. Please check your configuration.")
        sys.exit(1)

    print("✅ Environment setup complete")

    # Run the example
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Example interrupted by user")
    except Exception as e:
        print(f"\n💥 Example failed: {e}")
        import traceback

        traceback.print_exc()
