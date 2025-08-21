"""
CrewAI Integration Layer for Qdrant Memory System
Provides seamless integration between CrewAI and our enhanced memory system
"""

from typing import Any, Dict, List, Optional
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.entity.entity_memory import EntityMemory
from crewai.memory.short_term.short_term_memory import ShortTermMemory
from crewai.memory.long_term.long_term_memory import LongTermMemory
from .qdrant_storage import QdrantMemoryStorage, QdrantMemoryManager


class CrewAIQdrantStorage(RAGStorage):
    """
    CrewAI-compatible storage using Qdrant
    Extends CrewAI's RAGStorage to use our Qdrant implementation
    """

    def __init__(
        self,
        memory_type: str,
        allow_reset: bool = True,
        embedder_config: Optional[Dict] = None,
        crew=None,
    ):
        """
        Initialize CrewAI-compatible Qdrant storage

        Args:
            memory_type: Type of memory (entity, short_term, long_term, etc.)
            allow_reset: Whether to allow collection reset
            embedder_config: Embedding configuration
            crew: Crew instance for context
        """
        super().__init__(memory_type, allow_reset, embedder_config, crew)
        self.qdrant_storage = QdrantMemoryStorage(collection_name=memory_type)

    def search(
        self,
        query: str,
        limit: int = 3,
        filter: Optional[dict] = None,
        score_threshold: float = 0.7,
    ) -> List[Any]:
        """
        Search memory using semantic similarity

        Args:
            query: Search query
            limit: Maximum results
            filter: Metadata filter
            score_threshold: Minimum similarity score

        Returns:
            List of matching memory entries
        """
        if filter:
            results = self.qdrant_storage.retrieve_by_filter(filter, limit)
        else:
            results = self.qdrant_storage.retrieve(query, limit, score_threshold)

        # Convert to CrewAI format
        crewai_results = []
        for result in results:
            crewai_results.append(
                {
                    "id": result["id"],
                    "metadata": result["metadata"],
                    "context": result["content"],
                    "score": result.get("score", 1.0),
                }
            )

        return crewai_results

    def save(self, value: Any, metadata: Dict[str, Any]) -> None:
        """
        Save memory entry

        Args:
            value: Memory content
            metadata: Associated metadata
        """
        self.qdrant_storage.save(value, metadata)

    def reset(self) -> None:
        """Reset the memory collection"""
        if self.allow_reset:
            self.qdrant_storage.reset()


class EnhancedEntityMemory(EntityMemory):
    """
    Enhanced entity memory with Qdrant storage
    Provides better entity tracking and relationship mapping
    """

    def __init__(self, storage: Optional[CrewAIQdrantStorage] = None):
        """
        Initialize enhanced entity memory

        Args:
            storage: Qdrant storage instance
        """
        if storage is None:
            storage = CrewAIQdrantStorage("entity_memory")

        super().__init__(storage=storage)

    def add_entity(
        self,
        entity_name: str,
        entity_info: Dict[str, Any],
        relationships: Optional[List[str]] = None,
    ):
        """
        Add entity with enhanced information

        Args:
            entity_name: Name of the entity
            entity_info: Entity information
            relationships: Related entities
        """
        metadata = {
            "entity_name": entity_name,
            "entity_type": entity_info.get("type", "unknown"),
            "relationships": relationships or [],
            "created_at": entity_info.get("created_at"),
            "last_updated": entity_info.get("last_updated"),
        }

        self.storage.save(entity_info, metadata)

    def get_entity_context(self, entity_name: str, limit: int = 5) -> List[Dict]:
        """
        Get context for specific entity

        Args:
            entity_name: Name of the entity
            limit: Maximum results

        Returns:
            List of entity contexts
        """
        return self.storage.search(f"entity: {entity_name}", limit=limit)


class EnhancedShortTermMemory(ShortTermMemory):
    """
    Enhanced short-term memory with Qdrant storage
    Provides better session context management
    """

    def __init__(self, storage: Optional[CrewAIQdrantStorage] = None):
        """
        Initialize enhanced short-term memory

        Args:
            storage: Qdrant storage instance
        """
        if storage is None:
            storage = CrewAIQdrantStorage("short_term_memory")

        super().__init__(storage=storage)

    def add_interaction(
        self, agent_name: str, action: str, context: str, result: Optional[str] = None
    ):
        """
        Add interaction to short-term memory

        Args:
            agent_name: Name of the agent
            action: Action performed
            context: Context of the action
            result: Result of the action
        """
        interaction_data = {
            "agent": agent_name,
            "action": action,
            "context": context,
            "result": result,
            "timestamp": self._get_timestamp(),
        }

        metadata = {
            "memory_type": "interaction",
            "agent": agent_name,
            "session_id": self._get_session_id(),
        }

        self.storage.save(interaction_data, metadata)

    def get_recent_context(self, limit: int = 10) -> List[Dict]:
        """
        Get recent interactions for context

        Args:
            limit: Maximum results

        Returns:
            List of recent interactions
        """
        return self.storage.search("recent interactions", limit=limit)


class EnhancedLongTermMemory(LongTermMemory):
    """
    Enhanced long-term memory with Qdrant storage
    Provides persistent knowledge retention
    """

    def __init__(self, storage: Optional[CrewAIQdrantStorage] = None):
        """
        Initialize enhanced long-term memory

        Args:
            storage: Qdrant storage instance
        """
        if storage is None:
            storage = CrewAIQdrantStorage("long_term_memory")

        super().__init__(storage=storage)

    def add_knowledge(
        self,
        knowledge_type: str,
        content: str,
        source: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        """
        Add knowledge to long-term memory

        Args:
            knowledge_type: Type of knowledge
            content: Knowledge content
            source: Source of knowledge
            tags: Associated tags
        """
        knowledge_data = {
            "type": knowledge_type,
            "content": content,
            "source": source,
            "tags": tags or [],
            "timestamp": self._get_timestamp(),
        }

        metadata = {
            "memory_type": "knowledge",
            "knowledge_type": knowledge_type,
            "source": source,
            "tags": tags or [],
        }

        self.storage.save(knowledge_data, metadata)

    def search_knowledge(
        self, query: str, knowledge_type: Optional[str] = None, limit: int = 5
    ) -> List[Dict]:
        """
        Search knowledge in long-term memory

        Args:
            query: Search query
            knowledge_type: Filter by knowledge type
            limit: Maximum results

        Returns:
            List of matching knowledge entries
        """
        if knowledge_type:
            filter_dict = {"knowledge_type": knowledge_type}
            results = self.storage.retrieve_by_filter(filter_dict, limit)
        else:
            results = self.storage.retrieve(query, limit)

        return results


class CodeSnippetsMemory:
    """
    Specialized memory for code snippets and patterns
    """

    def __init__(self):
        """Initialize code snippets memory"""
        self.storage = QdrantMemoryStorage("code_snippets")

    def add_code_pattern(
        self,
        pattern_name: str,
        code: str,
        language: str,
        description: str,
        use_cases: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ):
        """
        Add code pattern to memory

        Args:
            pattern_name: Name of the pattern
            code: Code snippet
            language: Programming language
            description: Pattern description
            use_cases: Use cases for the pattern
            tags: Associated tags
        """
        pattern_data = {
            "name": pattern_name,
            "code": code,
            "language": language,
            "description": description,
            "use_cases": use_cases or [],
            "tags": tags or [],
            "timestamp": self._get_timestamp(),
        }

        metadata = {
            "memory_type": "code_pattern",
            "language": language,
            "pattern_name": pattern_name,
            "tags": tags or [],
        }

        self.storage.save(pattern_data, metadata)

    def find_code_pattern(
        self, query: str, language: Optional[str] = None, limit: int = 5
    ) -> List[Dict]:
        """
        Find code patterns

        Args:
            query: Search query
            language: Filter by programming language
            limit: Maximum results

        Returns:
            List of matching code patterns
        """
        if language:
            filter_dict = {"language": language}
            results = self.storage.retrieve_by_filter(filter_dict, limit)
        else:
            results = self.storage.retrieve(query, limit)

        return results


class DebuggingHistoryMemory:
    """
    Specialized memory for debugging history and error patterns
    """

    def __init__(self):
        """Initialize debugging history memory"""
        self.storage = QdrantMemoryStorage("debugging_history")

    def add_error_pattern(
        self,
        error_type: str,
        error_message: str,
        solution: str,
        context: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        """
        Add error pattern to memory

        Args:
            error_type: Type of error
            error_message: Error message
            solution: Solution to the error
            context: Error context
            tags: Associated tags
        """
        error_data = {
            "error_type": error_type,
            "error_message": error_message,
            "solution": solution,
            "context": context,
            "tags": tags or [],
            "timestamp": self._get_timestamp(),
        }

        metadata = {
            "memory_type": "error_pattern",
            "error_type": error_type,
            "tags": tags or [],
        }

        self.storage.save(error_data, metadata)

    def find_solution(self, error_message: str, limit: int = 3) -> List[Dict]:
        """
        Find solution for error

        Args:
            error_message: Error message to search for
            limit: Maximum results

        Returns:
            List of matching solutions
        """
        return self.storage.retrieve(error_message, limit)


class ProjectContextMemory:
    """
    Specialized memory for project-specific context
    """

    def __init__(self):
        """Initialize project context memory"""
        self.storage = QdrantMemoryStorage("project_context")

    def add_project_info(
        self,
        project_name: str,
        info_type: str,
        content: str,
        metadata: Optional[Dict] = None,
    ):
        """
        Add project information

        Args:
            project_name: Name of the project
            info_type: Type of information
            content: Information content
            metadata: Additional metadata
        """
        project_data = {
            "project_name": project_name,
            "info_type": info_type,
            "content": content,
            "timestamp": self._get_timestamp(),
        }

        if metadata:
            project_data.update(metadata)

        storage_metadata = {
            "memory_type": "project_info",
            "project_name": project_name,
            "info_type": info_type,
        }

        self.storage.save(project_data, storage_metadata)

    def get_project_context(
        self, project_name: str, info_type: Optional[str] = None, limit: int = 10
    ) -> List[Dict]:
        """
        Get project context

        Args:
            project_name: Name of the project
            info_type: Filter by information type
            limit: Maximum results

        Returns:
            List of project information
        """
        if info_type:
            filter_dict = {"project_name": project_name, "info_type": info_type}
            results = self.storage.retrieve_by_filter(filter_dict, limit)
        else:
            filter_dict = {"project_name": project_name}
            results = self.storage.retrieve_by_filter(filter_dict, limit)

        return results


class AgentCommunicationMemory:
    """
    Specialized memory for inter-agent communication
    """

    def __init__(self):
        """Initialize agent communication memory"""
        self.storage = QdrantMemoryStorage("agent_communication")

    def add_communication(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        message_type: str = "task",
        result: Optional[str] = None,
    ):
        """
        Add communication between agents

        Args:
            from_agent: Sending agent
            to_agent: Receiving agent
            message: Communication message
            message_type: Type of message
            result: Result of the communication
        """
        comm_data = {
            "from_agent": from_agent,
            "to_agent": to_agent,
            "message": message,
            "message_type": message_type,
            "result": result,
            "timestamp": self._get_timestamp(),
        }

        metadata = {
            "memory_type": "communication",
            "from_agent": from_agent,
            "to_agent": to_agent,
            "message_type": message_type,
        }

        self.storage.save(comm_data, metadata)

    def get_communication_history(
        self, agent_name: Optional[str] = None, limit: int = 20
    ) -> List[Dict]:
        """
        Get communication history

        Args:
            agent_name: Filter by agent name
            limit: Maximum results

        Returns:
            List of communications
        """
        if agent_name:
            filter_dict = {"from_agent": agent_name}
            results = self.storage.retrieve_by_filter(filter_dict, limit)
        else:
            results = self.storage.retrieve("communication history", limit)

        return results


class WorkflowPatternsMemory:
    """
    Specialized memory for successful workflow patterns
    """

    def __init__(self):
        """Initialize workflow patterns memory"""
        self.storage = QdrantMemoryStorage("workflow_patterns")

    def add_workflow_pattern(
        self,
        pattern_name: str,
        steps: List[str],
        success_rate: float,
        context: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        """
        Add workflow pattern

        Args:
            pattern_name: Name of the workflow pattern
            steps: List of workflow steps
            success_rate: Success rate of the pattern
            context: Pattern context
            tags: Associated tags
        """
        pattern_data = {
            "name": pattern_name,
            "steps": steps,
            "success_rate": success_rate,
            "context": context,
            "tags": tags or [],
            "timestamp": self._get_timestamp(),
        }

        metadata = {
            "memory_type": "workflow_pattern",
            "pattern_name": pattern_name,
            "success_rate": success_rate,
            "tags": tags or [],
        }

        self.storage.save(pattern_data, metadata)

    def find_workflow_pattern(
        self, query: str, min_success_rate: float = 0.7, limit: int = 5
    ) -> List[Dict]:
        """
        Find workflow patterns

        Args:
            query: Search query
            min_success_rate: Minimum success rate
            limit: Maximum results

        Returns:
            List of matching workflow patterns
        """
        results = self.storage.retrieve(query, limit)

        # Filter by success rate
        filtered_results = [
            result
            for result in results
            if result["metadata"].get("success_rate", 0) >= min_success_rate
        ]

        return filtered_results


def _get_timestamp():
    """Get current timestamp"""
    from datetime import datetime

    return datetime.now().isoformat()


def _get_session_id():
    """Get current session ID"""
    import uuid

    return str(uuid.uuid4())
