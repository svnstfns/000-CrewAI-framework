#!/bin/bash

# Multi-Agent Dashboard Quick Start Script
echo "🚀 Multi-Agent Dashboard Setup"
echo "=============================="
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Available commands:"
echo "  npm run dev    - Start development server (port 8080)"
echo "  npm start      - Start production server"
echo ""
echo "🌐 Opening dashboard in browser..."
npm run dev
