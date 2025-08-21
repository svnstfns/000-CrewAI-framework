"""
Qdrant Configuration for CrewAI Framework
Cloud SaaS configuration and credentials management
"""

import os
from typing import Optional


class QdrantConfig:
    """Configuration management for Qdrant cloud SaaS"""
    
    # Default cloud credentials (provided by user)
    DEFAULT_CLOUD_URL = "https://55182465-43a7-4ee6-9617-3dd69263e4f7.eu-central-1-0.aws.cloud.qdrant.io:6333"
    DEFAULT_CLOUD_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzYzNTgxMDU4fQ.D2nNPup_5bg2WPFAEsDYYi6xMa7_gPj8-X3d-Rd9Rms"
    DEFAULT_CLUSTER_ID = "55182465-43a7-4ee6-9617-3dd69263e4f7"
    
    @classmethod
    def get_cloud_url(cls) -> str:
        """Get Qdrant cloud URL from environment or use default"""
        return os.getenv("QDRANT_URL", cls.DEFAULT_CLOUD_URL)
    
    @classmethod
    def get_cloud_api_key(cls) -> str:
        """Get Qdrant cloud API key from environment or use default"""
        return os.getenv("QDRANT_API_KEY", cls.DEFAULT_CLOUD_API_KEY)
    
    @classmethod
    def get_cluster_id(cls) -> str:
        """Get Qdrant cluster ID from environment or use default"""
        return os.getenv("QDRANT_CLUSTER_ID", cls.DEFAULT_CLUSTER_ID)
    
    @classmethod
    def get_local_host(cls) -> str:
        """Get local Qdrant host from environment or use default"""
        return os.getenv("QDRANT_HOST", "localhost")
    
    @classmethod
    def get_local_port(cls) -> int:
        """Get local Qdrant port from environment or use default"""
        return int(os.getenv("QDRANT_PORT", "6333"))
    
    @classmethod
    def is_cloud_enabled(cls) -> bool:
        """Check if cloud configuration is available"""
        return bool(cls.get_cloud_api_key() and cls.get_cloud_url())
    
    @classmethod
    def get_connection_config(cls, use_cloud: bool = True) -> dict:
        """
        Get connection configuration for Qdrant
        
        Args:
            use_cloud: Whether to use cloud configuration (default: True)
            
        Returns:
            Dictionary with connection parameters
        """
        if use_cloud and cls.is_cloud_enabled():
            return {
                "url": cls.get_cloud_url(),
                "api_key": cls.get_cloud_api_key(),
                "host": None,
                "port": None
            }
        else:
            return {
                "url": None,
                "api_key": None,
                "host": cls.get_local_host(),
                "port": cls.get_local_port()
            }
    
    @classmethod
    def print_config(cls):
        """Print current configuration for debugging"""
        print("🔧 Qdrant Configuration:")
        print(f"   Cloud URL: {cls.get_cloud_url()}")
        print(f"   Cloud API Key: {cls.get_cloud_api_key()[:20]}...")
        print(f"   Cluster ID: {cls.get_cluster_id()}")
        print(f"   Local Host: {cls.get_local_host()}")
        print(f"   Local Port: {cls.get_local_port()}")
        print(f"   Cloud Enabled: {cls.is_cloud_enabled()}")


# Convenience functions for easy access
def get_qdrant_config(use_cloud: bool = True) -> dict:
    """Get Qdrant configuration for easy use in other modules"""
    return QdrantConfig.get_connection_config(use_cloud)


def is_qdrant_cloud_available() -> bool:
    """Check if Qdrant cloud is available"""
    return QdrantConfig.is_cloud_enabled()
