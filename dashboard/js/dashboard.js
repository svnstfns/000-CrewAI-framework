// dashboard.js - Main dashboard initialization and core functions

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Update time
    function updateTime() {
        const now = new Date();
        document.getElementById('current-time').textContent = 
            now.toTimeString().split(' ')[0];
    }
    setInterval(updateTime, 1000);
    updateTime();

    // Initialize all components
    initializeCharts();
    populateAgentGrid();
    populateAgentTable();
    startRealTimeUpdates();
    initializeInteractions();
});

// Populate agent grid
function populateAgentGrid() {
    const grid = document.getElementById('agent-grid');
    const agents = [
        { id: 'AGT-001', status: 'Processing', health: 95 },
        { id: 'AGT-002', status: 'Idle', health: 88 },
        { id: 'AGT-003', status: 'Processing', health: 92 },
        { id: 'AGT-004', status: 'Coordinating', health: 78 },
        { id: 'AGT-005', status: 'Processing', health: 91 },
        { id: 'AGT-006', status: 'Idle', health: 85 },
        { id: 'AGT-007', status: 'Processing', health: 94 },
        { id: 'AGT-008', status: 'Error Recovery', health: 65 }
    ];

    let html = '';
    agents.forEach(agent => {
        const healthClass = agent.health >= 80 ? 'healthy' : 'warning';
        html += `
            <div class="agent-card">
                <div class="agent-info">
                    <span class="agent-id">${agent.id}</span>
                    <span class="agent-status">${agent.status}</span>
                </div>
                <div class="agent-health ${healthClass}">${agent.health}%</div>
            </div>
        `;
    });
    grid.innerHTML = html;
}

// Populate agent table
function populateAgentTable() {
    const tbody = document.getElementById('agent-table');
    const agents = [
        { id: 'AGT-017', tasks: 142, cpu: 72, memory: 512, efficiency: 94.2, status: 'Optimal' },
        { id: 'AGT-023', tasks: 138, cpu: 68, memory: 489, efficiency: 92.8, status: 'Optimal' },
        { id: 'AGT-009', tasks: 134, cpu: 75, memory: 524, efficiency: 91.5, status: 'Optimal' },
        { id: 'AGT-041', tasks: 128, cpu: 65, memory: 456, efficiency: 89.7, status: 'Good' },
        { id: 'AGT-055', tasks: 124, cpu: 78, memory: 578, efficiency: 87.3, status: 'Good' }
    ];

    let html = '';
    agents.forEach(agent => {
        const statusColor = agent.status === 'Optimal' ? '#10b981' : '#f59e0b';
        html += `
            <tr>
                <td style="font-weight: 600">${agent.id}</td>
                <td>${agent.tasks}</td>
                <td>${agent.cpu}%</td>
                <td>${agent.memory}</td>
                <td>${agent.efficiency}%</td>
                <td style="color: ${statusColor}">${agent.status}</td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

// Initialize all interactive elements
function initializeInteractions() {
    // Component card interactions
    const componentCards = document.querySelectorAll('.component-card');
    componentCards.forEach(card => {
        card.addEventListener('click', function() {
            // Toggle component status on click
            if (this.classList.contains('error')) {
                this.classList.remove('error');
                this.classList.add('warning');
                this.querySelector('.component-status').textContent = 'Recovering';
                this.querySelector('.component-metric').textContent = 'Restarting...';
            } else if (this.classList.contains('warning')) {
                this.classList.remove('warning');
                this.classList.add('healthy');
                this.querySelector('.component-status').textContent = 'Operational';
                this.querySelector('.component-metric').textContent = '99.9% uptime';
            }
        });
    });

    // Task card hover effects
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.cursor = 'grab';
        });
        card.addEventListener('mousedown', function() {
            this.style.cursor = 'grabbing';
            this.style.opacity = '0.8';
        });
        card.addEventListener('mouseup', function() {
            this.style.cursor = 'grab';
            this.style.opacity = '1';
        });
    });

    // Pipeline control buttons
    const chartButtons = document.querySelectorAll('.chart-btn');
    chartButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from siblings
            this.parentElement.querySelectorAll('.chart-btn').forEach(b => {
                b.classList.remove('active');
            });
            // Add active class to clicked button
            this.classList.add('active');
        });
    });

    // Add click animation to requirement cards
    const reqCards = document.querySelectorAll('.requirement-card');
    reqCards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });
}
