# CrewAI Dashboard Integration Setup

## Requirements
```
crewai>=0.1.0
redis>=4.5.0
qdrant-client>=1.7.0
websockets>=11.0
numpy>=1.24.0
asyncio
```

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Redis:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

3. Start Qdrant:
```bash
docker run -d -p 6333:6333 qdrant/qdrant
```

4. Start WebSocket Server:
```bash
python websocket_server.py
```

5. Run CrewAI with monitoring:
```bash
python example_crew.py
```

6. Open Dashboard:
```bash
# In another terminal
cd ..
npm run dev
```

## Architecture

```
CrewAI Agents
     ↓
Redis + Qdrant
     ↓
WebSocket Server
     ↓
Dashboard UI
```

## Key Components

- `dashboard_agent.py`: Base agent class with monitoring
- `metrics_collector.py`: Metrics collection agent
- `websocket_server.py`: Real-time data streaming
- `qdrant_store.py`: Historical data storage
- `example_crew.py`: Example implementation
