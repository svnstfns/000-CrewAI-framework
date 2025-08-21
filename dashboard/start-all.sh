#!/bin/bash

# Multi-Agent Dashboard with CrewAI - Complete Setup Script

set -e  # Exit on error

echo "🚀 Multi-Agent Dashboard + CrewAI Integration Setup"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check prerequisites
echo "Checking prerequisites..."
echo "--------------------------"

# Check Docker
if command_exists docker; then
    print_status "Docker installed"
else
    print_error "Docker not found. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if command_exists docker-compose; then
    print_status "Docker Compose installed"
else
    print_error "Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Check Python
if command_exists python3; then
    print_status "Python3 installed"
else
    print_error "Python3 not found. Please install Python 3.8+ first."
    exit 1
fi

# Check Node.js
if command_exists node; then
    print_status "Node.js installed"
else
    print_warning "Node.js not found. Dashboard may not run optimally."
fi

echo ""
echo "Starting services..."
echo "--------------------"

# Start Docker services
echo "Starting Redis and Qdrant..."
cd crewai_integration
docker-compose up -d redis qdrant

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 5

# Check if Redis is running
if docker exec dashboard-redis redis-cli ping > /dev/null 2>&1; then
    print_status "Redis is running"
else
    print_error "Redis failed to start"
    exit 1
fi

# Check if Qdrant is running
if curl -s http://localhost:6333/health > /dev/null 2>&1; then
    print_status "Qdrant is running"
else
    print_warning "Qdrant may still be starting..."
fi

echo ""
echo "Setting up Python environment..."
echo "---------------------------------"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
print_status "Python dependencies installed"

echo ""
echo "Starting WebSocket server..."
echo "-----------------------------"

# Start WebSocket server in background
python websocket_server.py &
WS_PID=$!
print_status "WebSocket server started (PID: $WS_PID)"

# Go back to main directory
cd ..

echo ""
echo "Starting Dashboard UI..."
echo "------------------------"

# Install npm dependencies if needed
if [ -f "package.json" ]; then
    if [ ! -d "node_modules" ]; then
        echo "Installing npm dependencies..."
        npm install
        print_status "npm dependencies installed"
    fi
    
    # Start dashboard
    npm run dev &
    UI_PID=$!
    print_status "Dashboard UI started (PID: $UI_PID)"
else
    # Fallback to Python HTTP server
    echo "Starting Python HTTP server..."
    python3 -m http.server 8080 &
    UI_PID=$!
    print_status "Dashboard UI started on http://localhost:8080 (PID: $UI_PID)"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo "=================================================="
echo ""
echo "📊 Dashboard: http://localhost:8080"
echo "🔌 WebSocket: ws://localhost:8765"
echo "🗄️  Redis: localhost:6379"
echo "📦 Qdrant: http://localhost:6333"
echo "🔍 Redis Commander: http://localhost:8081"
echo ""
echo "To run CrewAI with monitoring:"
echo "  cd crewai_integration"
echo "  source venv/bin/activate"
echo "  python example_crew.py"
echo ""
echo "To stop all services:"
echo "  Press Ctrl+C"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down services..."
    
    # Kill WebSocket server
    if [ ! -z "$WS_PID" ]; then
        kill $WS_PID 2>/dev/null || true
        print_status "WebSocket server stopped"
    fi
    
    # Kill UI server
    if [ ! -z "$UI_PID" ]; then
        kill $UI_PID 2>/dev/null || true
        print_status "Dashboard UI stopped"
    fi
    
    # Stop Docker containers
    cd crewai_integration
    docker-compose down
    print_status "Docker services stopped"
    
    echo ""
    echo "Goodbye! 👋"
}

# Set up trap to cleanup on exit
trap cleanup EXIT

# Wait for user to stop
echo "Press Ctrl+C to stop all services..."
wait
