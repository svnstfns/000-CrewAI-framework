// websocket-client.js - WebSocket client for CrewAI integration

class CrewAIDashboardClient {
    constructor(wsUrl = 'ws://localhost:8765') {
        this.wsUrl = wsUrl;
        this.ws = null;
        this.reconnectInterval = 5000;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.isConnected = false;
        
        // Start connection
        this.connect();
        
        // Ping interval to keep connection alive
        this.pingInterval = setInterval(() => {
            if (this.isConnected) {
                this.send({ type: 'ping' });
            }
        }, 30000);
    }
    
    connect() {
        console.log(`[WS] Connecting to ${this.wsUrl}...`);
        
        try {
            this.ws = new WebSocket(this.wsUrl);
            
            this.ws.onopen = (event) => {
                console.log('[WS] Connected to CrewAI WebSocket server');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.onConnect();
                
                // Update UI connection status
                this.updateConnectionStatus(true);
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (error) {
                    console.error('[WS] Error parsing message:', error);
                }
            };
            
            this.ws.onerror = (error) => {
                console.error('[WS] WebSocket error:', error);
                this.isConnected = false;
            };
            
            this.ws.onclose = (event) => {
                console.log('[WS] Connection closed');
                this.isConnected = false;
                this.updateConnectionStatus(false);
                
                // Attempt reconnection
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.reconnectAttempts++;
                    console.log(`[WS] Reconnecting in ${this.reconnectInterval/1000}s... (Attempt ${this.reconnectAttempts})`);
                    setTimeout(() => this.connect(), this.reconnectInterval);
                }
            };
        } catch (error) {
            console.error('[WS] Failed to create WebSocket:', error);
        }
    }
    
    onConnect() {
        // Request initial data
        this.send({ type: 'get_metrics' });
    }
    
    handleMessage(data) {
        console.log('[WS] Received:', data.type);
        
        switch(data.type) {
            case 'initial':
                this.handleInitialData(data);
                break;
                
            case 'metric_update':
                this.handleMetricUpdate(data);
                break;
                
            case 'task_update':
                this.handleTaskUpdate(data);
                break;
                
            case 'system_update':
                this.handleSystemUpdate(data);
                break;
                
            case 'pipeline_update':
                this.handlePipelineUpdate(data);
                break;
                
            case 'pong':
                // Heartbeat response
                break;
                
            default:
                console.log('[WS] Unknown message type:', data.type);
        }
    }
    
    handleInitialData(data) {
        console.log('[WS] Received initial data');
        
        // Update system metrics
        if (data.system_metrics) {
            this.updateSystemMetrics(data.system_metrics);
        }
        
        // Update agent metrics
        if (data.agents) {
            this.updateAgentMetrics(data.agents);
        }
        
        // Update recent tasks
        if (data.recent_tasks) {
            this.updateRecentTasks(data.recent_tasks);
        }
    }
    
    handleMetricUpdate(data) {
        // Update specific metric
        if (data.agent_id) {
            // Agent-specific metric
            this.updateAgentMetric(data.agent_id, data);
        } else {
            // System metric
            this.updateSystemMetric(data);
        }
    }
    
    handleTaskUpdate(data) {
        // Update task status
        const taskId = data.task_id;
        const status = data.status;
        
        // Find task element and update
        const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
        if (taskElement) {
            // Update task card
            taskElement.className = `task-card ${status}`;
            
            // Move to appropriate column
            let targetColumn;
            switch(status) {
                case 'backlog':
                    targetColumn = document.querySelector('.kanban-column:nth-child(1)');
                    break;
                case 'in_progress':
                    targetColumn = document.querySelector('.kanban-column:nth-child(2)');
                    break;
                case 'testing':
                    targetColumn = document.querySelector('.kanban-column:nth-child(3)');
                    break;
                case 'done':
                case 'failed':
                    targetColumn = document.querySelector('.kanban-column:nth-child(4)');
                    break;
            }
            
            if (targetColumn) {
                targetColumn.appendChild(taskElement);
            }
        } else {
            // Create new task card
            this.createTaskCard(data);
        }
        
        // Flash update animation
        this.flashElement(`task-${taskId}`);
    }
    
    handleSystemUpdate(data) {
        // Update system-wide metrics
        if (data.system_tcr !== undefined) {
            this.updateMetricValue('tcr', data.system_tcr.toFixed(1) + '%');
        }
        
        if (data.system_velocity !== undefined) {
            this.updateMetricValue('velocity', Math.round(data.system_velocity));
        }
        
        if (data.total_agents !== undefined) {
            document.getElementById('total-agents').textContent = data.total_agents;
        }
    }
    
    handlePipelineUpdate(data) {
        const stage = data.stage;
        const status = data.status;
        
        // Update pipeline stage
        const stageElement = document.querySelector(`[data-stage="${stage}"]`);
        if (stageElement) {
            stageElement.className = `pipeline-stage ${status}`;
            const icon = stageElement.querySelector('.stage-icon');
            if (icon) {
                icon.textContent = status === 'completed' ? '✓' : 
                                  status === 'running' ? '⟳' : 
                                  status === 'failed' ? '✗' : '○';
            }
        }
    }
    
    updateSystemMetrics(metrics) {
        // Update all system metrics
        for (const [key, value] of Object.entries(metrics)) {
            const element = document.getElementById(key);
            if (element) {
                element.textContent = value;
                this.flashElement(key);
            }
        }
    }
    
    updateAgentMetrics(agents) {
        // Update agent-specific metrics
        for (const [agentId, metrics] of Object.entries(agents)) {
            this.updateAgentMetric(agentId, metrics);
        }
    }
    
    updateAgentMetric(agentId, metrics) {
        // Find or create agent card
        let agentCard = document.querySelector(`[data-agent-id="${agentId}"]`);
        
        if (!agentCard) {
            // Create new agent card
            this.createAgentCard(agentId, metrics);
        } else {
            // Update existing card
            if (metrics.task_completion_rate !== undefined) {
                const tcrElement = agentCard.querySelector('.agent-tcr');
                if (tcrElement) {
                    tcrElement.textContent = metrics.task_completion_rate.toFixed(1) + '%';
                }
            }
        }
    }
    
    updateRecentTasks(tasks) {
        // Clear existing tasks in kanban
        const kanbanColumns = document.querySelectorAll('.kanban-column');
        kanbanColumns.forEach(column => {
            const cards = column.querySelectorAll('.task-card');
            cards.forEach(card => card.remove());
        });
        
        // Add tasks to appropriate columns
        tasks.forEach(task => {
            this.createTaskCard(task);
        });
    }
    
    createTaskCard(taskData) {
        const card = document.createElement('div');
        card.className = `task-card ${taskData.status}`;
        card.setAttribute('data-task-id', taskData.task_id);
        
        card.innerHTML = `
            <span class="task-id">${taskData.task_id}</span>
            <span class="task-title">${taskData.description || 'Task'}</span>
            <div class="task-tags">
                <span class="tag">${taskData.agent}</span>
                ${taskData.duration ? `<span class="tag">${taskData.duration.toFixed(1)}s</span>` : ''}
            </div>
        `;
        
        // Add to appropriate column
        let columnIndex = 0;
        switch(taskData.status) {
            case 'backlog': columnIndex = 0; break;
            case 'in_progress': columnIndex = 1; break;
            case 'testing': columnIndex = 2; break;
            case 'done':
            case 'failed': columnIndex = 3; break;
        }
        
        const column = document.querySelectorAll('.kanban-column')[columnIndex];
        if (column) {
            column.appendChild(card);
        }
    }
    
    createAgentCard(agentId, metrics) {
        const grid = document.getElementById('agent-grid');
        if (!grid) return;
        
        const card = document.createElement('div');
        card.className = 'agent-card';
        card.setAttribute('data-agent-id', agentId);
        
        const tcr = metrics.task_completion_rate || 0;
        const healthClass = tcr >= 80 ? 'healthy' : 'warning';
        
        card.innerHTML = `
            <div class="agent-info">
                <span class="agent-id">${agentId}</span>
                <span class="agent-status">Active</span>
            </div>
            <div class="agent-health ${healthClass}">
                <span class="agent-tcr">${tcr.toFixed(1)}%</span>
            </div>
        `;
        
        grid.appendChild(card);
    }
    
    updateMetricValue(metricId, value) {
        const element = document.getElementById(metricId);
        if (element) {
            element.textContent = value;
            this.flashElement(metricId);
        }
    }
    
    flashElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.transition = 'color 0.3s ease';
            element.style.color = '#3b82f6';
            setTimeout(() => {
                element.style.color = '';
            }, 300);
        }
    }
    
    updateConnectionStatus(connected) {
        const indicator = document.querySelector('.status-indicator');
        if (indicator) {
            if (connected) {
                indicator.classList.add('active');
                indicator.style.background = '#10b981';
            } else {
                indicator.classList.remove('active');
                indicator.style.background = '#ef4444';
            }
        }
        
        // Update status text
        const statusText = document.querySelector('.status-item span:last-child');
        if (statusText) {
            statusText.textContent = connected ? 'System Online' : 'Connecting...';
        }
    }
    
    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.warn('[WS] Cannot send message - connection not open');
        }
    }
    
    disconnect() {
        if (this.pingInterval) {
            clearInterval(this.pingInterval);
        }
        
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Try to connect to WebSocket server
    window.crewAIClient = new CrewAIDashboardClient();
    
    console.log('CrewAI Dashboard Client initialized');
    console.log('Attempting to connect to WebSocket server...');
});
