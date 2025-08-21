"""
Qdrant Storage Implementation for CrewAI Memory Integration
Provides vector-based memory storage with multiple collection types
"""

from typing import Any, Dict, List, Optional, Union
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import json
import uuid
from datetime import datetime
from config.qdrant_config import get_qdrant_config, is_qdrant_cloud_available


class QdrantMemoryStorage:
    """
    Enhanced Qdrant storage for CrewAI memory management
    Supports multiple memory types with specialized collections
    """

    def __init__(
        self,
        collection_name: str,
        url: str = None,
        api_key: str = None,
        host: str = None,
        port: int = None,
        use_cloud: bool = True,
    ):
        """
        Initialize Qdrant storage for a specific memory type
        Supports both cloud (SaaS) and local deployments

        Args:
            collection_name: Name of the memory collection
            url: Qdrant cloud URL (for SaaS deployment)
            api_key: Qdrant cloud API key (for SaaS deployment)
            host: Qdrant server host (for local deployment)
            port: Qdrant server port (for local deployment)
            use_cloud: Whether to use cloud configuration (default: True)
        """
        self.collection_name = collection_name

        # Get configuration
        if url is None and api_key is None and host is None and port is None:
            # Use configuration system
            config = get_qdrant_config(use_cloud)
            url = config["url"]
            api_key = config["api_key"]
            host = config["host"]
            port = config["port"]

        # Use cloud configuration by default, fallback to local if specified
        if host and port:
            # Local deployment
            self.client = QdrantClient(host=host, port=port)
        else:
            # Cloud deployment (SaaS)
            self.client = QdrantClient(url=url, api_key=api_key)

        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection with proper configuration"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection with optimized settings
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=1536,  # OpenAI embedding size
                        distance=Distance.COSINE,
                    ),
                    optimizers_config={
                        "default_segment_number": 2,
                        "memmap_threshold": 20000,
                    },
                )
                print(f"Created collection: {self.collection_name}")
            else:
                print(f"Using existing collection: {self.collection_name}")

        except Exception as e:
            print(f"Error initializing collection {self.collection_name}: {e}")
            raise

    def save(self, data: Union[str, Dict], metadata: Optional[Dict] = None) -> str:
        """
        Save data to Qdrant with automatic embedding

        Args:
            data: Data to store (string or dict)
            metadata: Additional metadata

        Returns:
            str: ID of the saved record
        """
        try:
            # Generate unique ID
            record_id = str(uuid.uuid4())

            # Prepare metadata
            if metadata is None:
                metadata = {}

            # Add timestamp
            metadata["timestamp"] = datetime.now().isoformat()
            metadata["collection"] = self.collection_name

            # Convert data to string if needed
            if isinstance(data, dict):
                content = json.dumps(data, ensure_ascii=False)
                metadata["data_type"] = "dict"
            else:
                content = str(data)
                metadata["data_type"] = "string"

            # Create point with embedding
            point = PointStruct(
                id=record_id,
                vector=self._get_embedding(content),
                payload={"content": content, "metadata": metadata},
            )

            # Add to collection
            self.client.upsert(collection_name=self.collection_name, points=[point])

            return record_id

        except Exception as e:
            print(f"Error saving to {self.collection_name}: {e}")
            raise

    def retrieve(
        self, query: str, limit: int = 5, score_threshold: float = 0.7
    ) -> List[Dict]:
        """
        Retrieve data using semantic search

        Args:
            query: Search query
            limit: Maximum number of results
            score_threshold: Minimum similarity score

        Returns:
            List of matching records with scores
        """
        try:
            # Get query embedding
            query_vector = self._get_embedding(query)

            # Search in collection
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
            )

            # Format results
            results = []
            for point in search_result:
                result = {
                    "id": point.id,
                    "score": point.score,
                    "content": point.payload.get("content"),
                    "metadata": point.payload.get("metadata", {}),
                }

                # Parse content if it's JSON
                if result["metadata"].get("data_type") == "dict":
                    try:
                        result["content"] = json.loads(result["content"])
                    except:
                        pass

                results.append(result)

            return results

        except Exception as e:
            print(f"Error retrieving from {self.collection_name}: {e}")
            return []

    def retrieve_by_filter(self, filter_dict: Dict, limit: int = 10) -> List[Dict]:
        """
        Retrieve data using metadata filters

        Args:
            filter_dict: Filter conditions
            limit: Maximum number of results

        Returns:
            List of matching records
        """
        try:
            # Build filter
            conditions = []
            for key, value in filter_dict.items():
                conditions.append(
                    FieldCondition(key=f"metadata.{key}", match=MatchValue(value=value))
                )

            filter_obj = Filter(must=conditions) if conditions else None

            # Search with filter
            search_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=filter_obj,
                limit=limit,
            )

            # Format results
            results = []
            for point in search_result[0]:
                result = {
                    "id": point.id,
                    "content": point.payload.get("content"),
                    "metadata": point.payload.get("metadata", {}),
                }

                # Parse content if it's JSON
                if result["metadata"].get("data_type") == "dict":
                    try:
                        result["content"] = json.loads(result["content"])
                    except:
                        pass

                results.append(result)

            return results

        except Exception as e:
            print(f"Error filtering {self.collection_name}: {e}")
            return []

    def update(
        self, record_id: str, data: Union[str, Dict], metadata: Optional[Dict] = None
    ):
        """
        Update existing record

        Args:
            record_id: ID of record to update
            data: New data
            metadata: Updated metadata
        """
        try:
            # Get existing record
            existing = self.client.retrieve(
                collection_name=self.collection_name, ids=[record_id]
            )

            if not existing:
                raise ValueError(f"Record {record_id} not found")

            existing_point = existing[0]
            existing_metadata = existing_point.payload.get("metadata", {})

            # Update metadata
            if metadata:
                existing_metadata.update(metadata)
            existing_metadata["updated_at"] = datetime.now().isoformat()

            # Convert data to string if needed
            if isinstance(data, dict):
                content = json.dumps(data, ensure_ascii=False)
                existing_metadata["data_type"] = "dict"
            else:
                content = str(data)
                existing_metadata["data_type"] = "string"

            # Update point
            updated_point = PointStruct(
                id=record_id,
                vector=self._get_embedding(content),
                payload={"content": content, "metadata": existing_metadata},
            )

            self.client.upsert(
                collection_name=self.collection_name, points=[updated_point]
            )

        except Exception as e:
            print(f"Error updating record {record_id}: {e}")
            raise

    def delete(self, record_id: str):
        """
        Delete a record

        Args:
            record_id: ID of record to delete
        """
        try:
            self.client.delete(
                collection_name=self.collection_name, points_selector=[record_id]
            )
        except Exception as e:
            print(f"Error deleting record {record_id}: {e}")
            raise

    def reset(self):
        """Reset the entire collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self._initialize_collection()
            print(f"Reset collection: {self.collection_name}")
        except Exception as e:
            print(f"Error resetting collection {self.collection_name}: {e}")
            raise

    def get_stats(self) -> Dict:
        """
        Get collection statistics

        Returns:
            Dictionary with collection stats
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "status": info.status,
            }
        except Exception as e:
            print(f"Error getting stats for {self.collection_name}: {e}")
            return {}

    def _get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text using OpenAI

        Args:
            text: Text to embed

        Returns:
            List of embedding values
        """
        try:
            # Import OpenAI here to avoid circular imports
            from openai import OpenAI

            client = OpenAI()
            response = client.embeddings.create(
                model="text-embedding-ada-002", input=text
            )

            return response.data[0].embedding

        except Exception as e:
            print(f"Error getting embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 1536


class QdrantMemoryManager:
    """
    Manager for multiple Qdrant memory collections
    Provides unified interface for different memory types
    """

    def __init__(
        self,
        url: str = None,
        api_key: str = None,
        host: str = None,
        port: int = None,
        use_cloud: bool = True,
    ):
        """
        Initialize memory manager
        Supports both cloud (SaaS) and local deployments

        Args:
            url: Qdrant cloud URL (for SaaS deployment)
            api_key: Qdrant cloud API key (for SaaS deployment)
            host: Qdrant server host (for local deployment)
            port: Qdrant server port (for local deployment)
            use_cloud: Whether to use cloud configuration (default: True)
        """
        # Get configuration if not provided
        if url is None and api_key is None and host is None and port is None:
            config = get_qdrant_config(use_cloud)
            url = config["url"]
            api_key = config["api_key"]
            host = config["host"]
            port = config["port"]

        self.url = url
        self.api_key = api_key
        self.host = host
        self.port = port
        self.storages = {}
        self._initialize_memory_types()

    def _initialize_memory_types(self):
        """Initialize all memory type collections"""
        memory_types = [
            "entity_memory",
            "short_term_memory",
            "long_term_memory",
            "code_snippets",
            "debugging_history",
            "project_context",
            "agent_communication",
            "workflow_patterns",
        ]

        for memory_type in memory_types:
            self.storages[memory_type] = QdrantMemoryStorage(
                collection_name=memory_type,
                url=self.url,
                api_key=self.api_key,
                host=self.host,
                port=self.port,
            )

    def get_storage(self, memory_type: str) -> QdrantMemoryStorage:
        """
        Get storage for specific memory type

        Args:
            memory_type: Type of memory storage

        Returns:
            QdrantMemoryStorage instance
        """
        if memory_type not in self.storages:
            # Create new storage if it doesn't exist
            self.storages[memory_type] = QdrantMemoryStorage(
                collection_name=memory_type,
                url=self.url,
                api_key=self.api_key,
                host=self.host,
                port=self.port,
            )

        return self.storages[memory_type]

    def save_to_memory(
        self, memory_type: str, data: Union[str, Dict], metadata: Optional[Dict] = None
    ) -> str:
        """
        Save data to specific memory type

        Args:
            memory_type: Type of memory to save to
            data: Data to save
            metadata: Additional metadata

        Returns:
            str: ID of saved record
        """
        storage = self.get_storage(memory_type)
        return storage.save(data, metadata)

    def retrieve_from_memory(
        self, memory_type: str, query: str, limit: int = 5
    ) -> List[Dict]:
        """
        Retrieve data from specific memory type

        Args:
            memory_type: Type of memory to search
            query: Search query
            limit: Maximum results

        Returns:
            List of matching records
        """
        storage = self.get_storage(memory_type)
        return storage.retrieve(query, limit)

    def get_all_stats(self) -> Dict:
        """
        Get statistics for all memory collections

        Returns:
            Dictionary with stats for all collections
        """
        stats = {}
        for memory_type, storage in self.storages.items():
            stats[memory_type] = storage.get_stats()
        return stats

    def reset_all(self):
        """Reset all memory collections"""
        for storage in self.storages.values():
            storage.reset()
        print("Reset all memory collections")
