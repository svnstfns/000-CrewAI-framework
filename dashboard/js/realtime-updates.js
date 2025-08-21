// realtime-updates.js - Real-time update and animation functions

// Start real-time updates
function startRealTimeUpdates() {
    // Simulate WebSocket updates
    setInterval(() => {
        // Update metrics with slight variations
        updateMetric('tcr', 90, 98, '%');
        updateMetric('velocity', 1100, 1400, '');
        updateMetric('throughput', 38, 48, 'K');
        updateMetric('efficiency', 85, 92, '%');
        
        // Update agent count
        const agentCount = 240 + Math.floor(Math.random() * 30);
        document.getElementById('total-agents').textContent = agentCount;
    }, 2000);

    // Animate test progress
    animateTests();
    
    // Update CI/CD pipeline
    setInterval(updatePipeline, 5000);
    
    // Update requirements progress
    setInterval(updateRequirements, 3000);
}

// Update metric with animation
function updateMetric(id, min, max, suffix) {
    const element = document.getElementById(id);
    const value = (min + Math.random() * (max - min)).toFixed(1);
    
    if (id === 'coordination') {
        element.textContent = `${(4 + Math.random() * 0.8).toFixed(1)}/5`;
    } else if (id === 'ci-coefficient') {
        element.textContent = (1.4 + Math.random() * 0.4).toFixed(2);
    } else {
        element.textContent = value + suffix;
    }
    
    // Add flash effect
    element.style.transition = 'color 0.3s ease';
    element.style.color = '#3b82f6';
    setTimeout(() => {
        element.style.color = '#e8eaed';
    }, 300);
}

// Animate test execution
function animateTests() {
    // Simulate test execution
    let testProgress = 0;
    const testInterval = setInterval(() => {
        testProgress += Math.random() * 5;
        
        // Update test bars with animation
        const testBars = document.querySelectorAll('.test-progress.running');
        testBars.forEach(bar => {
            const currentWidth = parseFloat(bar.style.width) || 0;
            if (currentWidth < 90) {
                bar.style.width = Math.min(currentWidth + 2, 90) + '%';
            }
        });

        // Randomly mark some tests as passed
        if (Math.random() > 0.8) {
            const runningTests = document.querySelectorAll('.test-stat.running');
            if (runningTests.length > 0) {
                const test = runningTests[0];
                test.classList.remove('running');
                test.classList.add('passed');
                test.innerHTML = '✓ Test passed';
            }
        }
    }, 1000);
}

// Update CI/CD pipeline stages
function updatePipeline() {
    const stages = document.querySelectorAll('.pipeline-stage');
    let foundRunning = false;
    
    stages.forEach((stage, index) => {
        if (stage.classList.contains('running') && !foundRunning) {
            foundRunning = true;
            // Move to next stage randomly
            if (Math.random() > 0.7) {
                stage.classList.remove('running');
                stage.classList.add('completed');
                stage.querySelector('.stage-icon').textContent = '✓';
                
                // Update connector
                const connector = stage.nextElementSibling;
                if (connector && connector.classList.contains('pipeline-connector')) {
                    connector.classList.add('completed');
                }
                
                // Start next stage
                if (index < stages.length - 1) {
                    const nextStage = stages[index + 1];
                    if (nextStage.classList.contains('pending')) {
                        nextStage.classList.remove('pending');
                        nextStage.classList.add('running');
                        nextStage.querySelector('.stage-icon').textContent = '⟳';
                        nextStage.querySelector('.stage-time').textContent = 'Running...';
                    }
                }
            }
        }
    });
}

// Update requirement progress
function updateRequirements() {
    const progressBars = document.querySelectorAll('.requirement-card .progress-fill');
    progressBars.forEach(bar => {
        const currentWidth = parseFloat(bar.style.width) || 0;
        if (currentWidth < 100 && !bar.classList.contains('failed')) {
            const increment = Math.random() * 5;
            bar.style.width = Math.min(currentWidth + increment, 100) + '%';
            
            // Update status when complete
            if (currentWidth + increment >= 100) {
                const card = bar.closest('.requirement-card');
                const statusEl = card.querySelector('.req-status');
                if (statusEl.classList.contains('in-progress')) {
                    statusEl.classList.remove('in-progress');
                    statusEl.classList.add('done');
                    statusEl.textContent = 'DONE';
                    card.classList.remove('in-progress');
                    card.classList.add('done');
                }
            }
        }
    });
}

// WebSocket connection (placeholder for real implementation)
function initWebSocket(url) {
    // This is a placeholder for real WebSocket implementation
    // In production, you would connect to your actual WebSocket server
    
    // Example implementation:
    // const ws = new WebSocket(url);
    // 
    // ws.onopen = function(event) {
    //     console.log('Connected to WebSocket server');
    // };
    // 
    // ws.onmessage = function(event) {
    //     const data = JSON.parse(event.data);
    //     updateDashboard(data);
    // };
    // 
    // ws.onerror = function(error) {
    //     console.error('WebSocket error:', error);
    // };
    // 
    // ws.onclose = function(event) {
    //     console.log('WebSocket connection closed');
    //     // Implement reconnection logic here
    // };
    
    console.log('WebSocket ready for connection to:', url);
}

// Update dashboard with WebSocket data
function updateDashboard(data) {
    // Update metrics
    if (data.metrics) {
        if (data.metrics.tcr) {
            document.getElementById('tcr').textContent = data.metrics.tcr + '%';
        }
        if (data.metrics.velocity) {
            document.getElementById('velocity').textContent = data.metrics.velocity;
        }
        // Add more metric updates as needed
    }
    
    // Update agents
    if (data.agents) {
        document.getElementById('total-agents').textContent = data.agents.total;
        // Update agent grid if needed
    }
    
    // Update pipeline status
    if (data.pipeline) {
        // Update pipeline stages based on data
    }
}

// Export functions for external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        startRealTimeUpdates,
        updateMetric,
        initWebSocket,
        updateDashboard
    };
}
