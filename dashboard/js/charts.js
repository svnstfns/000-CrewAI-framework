// charts.js - Chart visualization functions

// Initialize all charts
function initializeCharts() {
    createTimelineChart();
    createGaugeChart();
    createNetworkGraph();
}

// Create timeline chart
function createTimelineChart() {
    const svg = document.getElementById('timeline-chart');
    const width = svg.clientWidth;
    const height = svg.clientHeight;
    const margin = { top: 20, right: 30, bottom: 30, left: 50 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;

    // Generate sample data
    const data = [];
    for (let i = 0; i < 60; i++) {
        data.push({
            time: i,
            tcr: 90 + Math.random() * 10,
            efficiency: 85 + Math.random() * 10,
            coordination: 4 + Math.random() * 0.8
        });
    }

    // Create SVG elements
    let svgContent = `
        <defs>
            <linearGradient id="gradient1" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:0.05" />
            </linearGradient>
            <linearGradient id="gradient2" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#10b981;stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:#10b981;stop-opacity:0.05" />
            </linearGradient>
        </defs>
        <g transform="translate(${margin.left},${margin.top})">
    `;

    // Draw grid lines
    for (let i = 0; i <= 4; i++) {
        const y = (chartHeight / 4) * i;
        svgContent += `
            <line x1="0" y1="${y}" x2="${chartWidth}" y2="${y}" 
                  stroke="#2a3344" stroke-width="1" opacity="0.5"/>
            <text x="-10" y="${y}" fill="#6b7280" font-size="10" text-anchor="end">
                ${100 - i * 25}%
            </text>
        `;
    }

    // Draw TCR area
    let pathData = `M 0 ${chartHeight - (data[0].tcr - 75) * (chartHeight / 25)}`;
    data.forEach((d, i) => {
        const x = (i / (data.length - 1)) * chartWidth;
        const y = chartHeight - (d.tcr - 75) * (chartHeight / 25);
        pathData += ` L ${x} ${y}`;
    });
    pathData += ` L ${chartWidth} ${chartHeight} L 0 ${chartHeight} Z`;
    
    svgContent += `<path d="${pathData}" fill="url(#gradient1)" opacity="0.8"/>`;

    // Draw TCR line
    let lineData = `M 0 ${chartHeight - (data[0].tcr - 75) * (chartHeight / 25)}`;
    data.forEach((d, i) => {
        const x = (i / (data.length - 1)) * chartWidth;
        const y = chartHeight - (d.tcr - 75) * (chartHeight / 25);
        lineData += ` L ${x} ${y}`;
    });
    
    svgContent += `<path d="${lineData}" fill="none" stroke="#3b82f6" stroke-width="2"/>`;

    // Draw Efficiency line
    let effLineData = `M 0 ${chartHeight - (data[0].efficiency - 75) * (chartHeight / 25)}`;
    data.forEach((d, i) => {
        const x = (i / (data.length - 1)) * chartWidth;
        const y = chartHeight - (d.efficiency - 75) * (chartHeight / 25);
        effLineData += ` L ${x} ${y}`;
    });
    
    svgContent += `<path d="${effLineData}" fill="none" stroke="#10b981" stroke-width="2"/>`;

    // Add legend
    svgContent += `
        <g transform="translate(${chartWidth - 150}, 10)">
            <rect x="0" y="0" width="12" height="12" fill="#3b82f6"/>
            <text x="18" y="10" fill="#e8eaed" font-size="12">Task Completion</text>
            <rect x="0" y="20" width="12" height="12" fill="#10b981"/>
            <text x="18" y="30" fill="#e8eaed" font-size="12">Efficiency</text>
        </g>
    `;

    svgContent += '</g>';
    svg.innerHTML = svgContent;
}

// Create gauge chart
function createGaugeChart() {
    const svg = document.getElementById('gauge-chart');
    const width = 250;
    const height = 200;
    const radius = 80;
    const centerX = width / 2;
    const centerY = height - 30;

    const value = 87; // System health percentage
    const angle = (value / 100) * 180 - 90;
    const angleRad = (angle * Math.PI) / 180;

    let svgContent = `
        <defs>
            <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#ef4444;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#f59e0b;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#10b981;stop-opacity:1" />
            </linearGradient>
        </defs>
    `;

    // Draw arc background
    svgContent += `
        <path d="M ${centerX - radius} ${centerY} 
                 A ${radius} ${radius} 0 0 1 ${centerX + radius} ${centerY}"
              fill="none" stroke="#2a3344" stroke-width="15" stroke-linecap="round"/>
    `;

    // Draw colored arc
    const endX = centerX + radius * Math.cos(angleRad);
    const endY = centerY + radius * Math.sin(angleRad);
    const largeArc = value > 50 ? 1 : 0;

    svgContent += `
        <path d="M ${centerX - radius} ${centerY} 
                 A ${radius} ${radius} 0 ${largeArc} 1 ${endX} ${endY}"
              fill="none" stroke="url(#gaugeGradient)" stroke-width="15" stroke-linecap="round"/>
    `;

    // Draw needle
    svgContent += `
        <line x1="${centerX}" y1="${centerY}" 
              x2="${endX}" y2="${endY}"
              stroke="#e8eaed" stroke-width="3" stroke-linecap="round"/>
        <circle cx="${centerX}" cy="${centerY}" r="8" fill="#e8eaed"/>
    `;

    // Add text
    svgContent += `
        <text x="${centerX}" y="${centerY - 20}" 
              text-anchor="middle" fill="#e8eaed" font-size="36" font-weight="700">
            ${value}%
        </text>
        <text x="${centerX}" y="${centerY + 15}" 
              text-anchor="middle" fill="#9ca3b4" font-size="12">
            System Health
        </text>
    `;

    svg.innerHTML = svgContent;
}

// Create network graph
function createNetworkGraph() {
    const svg = document.getElementById('network-graph');
    const container = svg.parentElement;
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);

    // Generate nodes
    const nodes = [];
    const nodeCount = 20;
    for (let i = 0; i < nodeCount; i++) {
        nodes.push({
            id: i,
            x: Math.random() * (width - 100) + 50,
            y: Math.random() * (height - 100) + 50,
            type: i === 0 ? 'master' : (Math.random() > 0.7 ? 'coordinator' : 'worker'),
            health: Math.random() > 0.2 ? 'healthy' : 'warning'
        });
    }

    // Generate connections
    let svgContent = '<g class="links">';
    nodes.forEach((node, i) => {
        if (i > 0) {
            const target = nodes[Math.floor(Math.random() * i)];
            svgContent += `
                <line x1="${node.x}" y1="${node.y}" 
                      x2="${target.x}" y2="${target.y}"
                      stroke="#2a3344" stroke-width="1" opacity="0.5"/>
            `;
        }
    });
    svgContent += '</g>';

    // Draw nodes
    svgContent += '<g class="nodes">';
    nodes.forEach(node => {
        const color = node.type === 'master' ? '#3b82f6' : 
                     node.type === 'coordinator' ? '#06b6d4' : '#6b7280';
        const size = node.type === 'master' ? 12 : 
                    node.type === 'coordinator' ? 10 : 8;
        
        svgContent += `
            <circle cx="${node.x}" cy="${node.y}" r="${size}"
                    fill="${color}" stroke="${color}" stroke-width="2" fill-opacity="0.8"/>
        `;
        
        // Add pulse effect for master node
        if (node.type === 'master') {
            svgContent += `
                <circle cx="${node.x}" cy="${node.y}" r="${size}"
                        fill="none" stroke="${color}" stroke-width="2" opacity="0.5">
                    <animate attributeName="r" 
                             values="${size};${size + 10};${size}" 
                             dur="2s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" 
                             values="0.5;0;0.5" 
                             dur="2s" repeatCount="indefinite"/>
                </circle>
            `;
        }
    });
    svgContent += '</g>';

    svg.innerHTML = svgContent;
}
