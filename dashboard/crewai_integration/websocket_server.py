#!/usr/bin/env python3
"""
WebSocket server that bridges Redis pub/sub with the Dashboard
"""

import asyncio
import websockets
import redis
import json
import threading
from datetime import datetime
from typing import Set, Dict, Any

class DashboardWebSocketServer:
    def __init__(self, redis_host='localhost', redis_port=6379, ws_port=8765):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.ws_port = ws_port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        
        # Redis clients (one for pub/sub, one for data)
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()
        
        # Subscribe to all dashboard channels
        self.pubsub.subscribe([
            'dashboard:metrics',
            'dashboard:tasks',
            'dashboard:system',
            'dashboard:pipeline',
            'dashboard:communication'
        ])
        
    async def register(self, websocket):
        """Register a new WebSocket client"""
        self.clients.add(websocket)
        print(f"[WS] Client connected from {websocket.remote_address}")
        
        # Send initial data
        await self.send_initial_data(websocket)
        
    async def unregister(self, websocket):
        """Unregister a WebSocket client"""
        if websocket in self.clients:
            self.clients.remove(websocket)
            print(f"[WS] Client disconnected from {websocket.remote_address}")
    
    async def send_initial_data(self, websocket):
        """Send initial dashboard state to new client"""
        try:
            # Get current system metrics
            system_metrics = self.redis_client.hgetall('system:metrics')
            
            # Get agent metrics
            agent_keys = self.redis_client.keys('agent:metrics:*')
            agents_data = {}
            for key in agent_keys:
                agent_name = key.split(':')[-1]
                agents_data[agent_name] = self.redis_client.hgetall(key)
            
            # Get recent tasks
            task_keys = self.redis_client.keys('task:*')[:10]
            tasks_data = []
            for key in task_keys:
                tasks_data.append(self.redis_client.hgetall(key))
            
            initial_data = {
                'type': 'initial',
                'timestamp': datetime.now().isoformat(),
                'system_metrics': system_metrics,
                'agents': agents_data,
                'recent_tasks': tasks_data
            }
            
            await websocket.send(json.dumps(initial_data))
            print(f"[WS] Sent initial data to client")
            
        except Exception as e:
            print(f"[WS] Error sending initial data: {e}")
    
    async def broadcast(self, message: str):
        """Broadcast message to all connected clients"""
        if self.clients:
            # Create tasks for all clients
            tasks = []
            for client in self.clients.copy():
                tasks.append(self.send_to_client(client, message))
            
            # Send to all clients concurrently
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_to_client(self, websocket, message):
        """Send message to a specific client"""
        try:
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            await self.unregister(websocket)
        except Exception as e:
            print(f"[WS] Error sending to client: {e}")
            await self.unregister(websocket)
    
    def redis_listener(self):
        """Listen to Redis pub/sub in a separate thread"""
        print("[Redis] Starting Redis listener...")
        
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                # Parse the message
                try:
                    data = json.loads(message['data'])
                    
                    # Add message type based on channel
                    channel = message['channel']
                    if 'metrics' in channel:
                        data['type'] = 'metric_update'
                    elif 'tasks' in channel:
                        data['type'] = 'task_update'
                    elif 'system' in channel:
                        data['type'] = 'system_update'
                    elif 'pipeline' in channel:
                        data['type'] = 'pipeline_update'
                    else:
                        data['type'] = 'general_update'
                    
                    # Broadcast to all WebSocket clients
                    asyncio.run_coroutine_threadsafe(
                        self.broadcast(json.dumps(data)),
                        self.loop
                    )
                    
                    print(f"[Redis] Broadcasted {data['type']} to {len(self.clients)} clients")
                    
                except json.JSONDecodeError as e:
                    print(f"[Redis] Error parsing message: {e}")
                except Exception as e:
                    print(f"[Redis] Error processing message: {e}")
    
    async def handle_client(self, websocket, path):
        """Handle a WebSocket client connection"""
        await self.register(websocket)
        try:
            async for message in websocket:
                # Handle client messages
                try:
                    data = json.loads(message)
                    await self.handle_client_message(websocket, data)
                except json.JSONDecodeError:
                    print(f"[WS] Invalid JSON from client: {message}")
                except Exception as e:
                    print(f"[WS] Error handling client message: {e}")
        finally:
            await self.unregister(websocket)
    
    async def handle_client_message(self, websocket, data: Dict[str, Any]):
        """Handle messages from WebSocket clients"""
        
        msg_type = data.get('type')
        
        if msg_type == 'ping':
            # Respond to ping
            await websocket.send(json.dumps({'type': 'pong'}))
            
        elif msg_type == 'get_metrics':
            # Send current metrics
            await self.send_initial_data(websocket)
            
        elif msg_type == 'get_tasks':
            # Get task history
            task_keys = self.redis_client.keys('task:*')
            tasks = []
            for key in task_keys[-50:]:  # Last 50 tasks
                tasks.append(self.redis_client.hgetall(key))
            
            await websocket.send(json.dumps({
                'type': 'task_history',
                'tasks': tasks
            }))
            
        else:
            print(f"[WS] Unknown message type: {msg_type}")
    
    async def start_server(self):
        """Start the WebSocket server"""
        print(f"[WS] Starting WebSocket server on port {self.ws_port}...")
        
        # Store event loop for Redis listener
        self.loop = asyncio.get_event_loop()
        
        # Start Redis listener in background thread
        redis_thread = threading.Thread(target=self.redis_listener, daemon=True)
        redis_thread.start()
        
        # Start WebSocket server
        async with websockets.serve(self.handle_client, 'localhost', self.ws_port):
            print(f"[WS] WebSocket server running on ws://localhost:{self.ws_port}")
            print("[WS] Waiting for connections...")
            await asyncio.Future()  # Run forever


def main():
    """Main entry point"""
    print("=" * 50)
    print("Multi-Agent Dashboard WebSocket Server")
    print("=" * 50)
    
    # Check Redis connection
    try:
        r = redis.Redis(host='localhost', port=6379)
        r.ping()
        print("✅ Redis connected")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        print("Please start Redis first:")
        print("  docker run -d -p 6379:6379 redis:7-alpine")
        return
    
    # Create and start server
    server = DashboardWebSocketServer()
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\n[WS] Shutting down server...")
    except Exception as e:
        print(f"[WS] Server error: {e}")


if __name__ == "__main__":
    main()
