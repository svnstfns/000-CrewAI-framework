#!/usr/bin/env python3
"""
Test script for Qdrant Cloud Configuration
Verifies that the cloud SaaS setup works correctly
"""

import asyncio
from config.qdrant_config import (
    QdrantConfig,
    get_qdrant_config,
    is_qdrant_cloud_available,
)
from memory.qdrant_storage import QdrantMemoryManager


def test_configuration():
    """Test the configuration system"""
    print("🧪 Testing Qdrant Configuration...")

    # Print current configuration
    QdrantConfig.print_config()

    # Test configuration functions
    print(f"\n✅ Cloud Available: {is_qdrant_cloud_available()}")

    # Get cloud config
    cloud_config = get_qdrant_config(use_cloud=True)
    print(f"✅ Cloud Config: {cloud_config}")

    # Get local config
    local_config = get_qdrant_config(use_cloud=False)
    print(f"✅ Local Config: {local_config}")


def test_memory_manager():
    """Test the memory manager with cloud configuration"""
    print("\n🧪 Testing Qdrant Memory Manager...")

    try:
        # Initialize memory manager with cloud config
        memory_manager = QdrantMemoryManager(use_cloud=True)
        print("✅ Memory Manager initialized successfully")

        # Test saving data
        test_data = "This is a test message for cloud Qdrant"
        test_metadata = {"test": True, "source": "cloud_test"}

        record_id = memory_manager.save_to_memory(
            "short_term_memory", test_data, test_metadata
        )
        print(f"✅ Data saved with ID: {record_id}")

        # Test retrieving data
        results = memory_manager.retrieve_from_memory(
            "short_term_memory", "test message", limit=5
        )
        print(f"✅ Retrieved {len(results)} results")

        # Test getting stats
        stats = memory_manager.get_all_stats()
        print(f"✅ Memory stats: {stats}")

        return True

    except Exception as e:
        print(f"❌ Error testing memory manager: {e}")
        return False


def test_direct_qdrant_connection():
    """Test direct connection to Qdrant cloud"""
    print("\n🧪 Testing Direct Qdrant Connection...")

    try:
        from qdrant_client import QdrantClient

        config = get_qdrant_config(use_cloud=True)
        client = QdrantClient(url=config["url"], api_key=config["api_key"])

        # Test connection by getting collections
        collections = client.get_collections()
        print(f"✅ Connected to Qdrant cloud successfully")
        print(f"✅ Found {len(collections.collections)} collections")

        for collection in collections.collections:
            print(f"   - {collection.name}")

        return True

    except Exception as e:
        print(f"❌ Error connecting to Qdrant cloud: {e}")
        return False


async def main():
    """Main test function"""
    print("🚀 Qdrant Cloud Configuration Test")
    print("=" * 50)

    # Test configuration
    test_configuration()

    # Test direct connection
    if test_direct_qdrant_connection():
        # Test memory manager
        test_memory_manager()

    print("\n✅ Cloud configuration test completed!")


if __name__ == "__main__":
    asyncio.run(main())
