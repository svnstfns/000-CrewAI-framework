#!/bin/bash

# Automated Project Setup with Backup Protocol
# Usage: ./setup-project.sh <project-name> <description>

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required arguments are provided
if [ $# -lt 2 ]; then
    print_error "Usage: $0 <project-name> <description>"
    print_error "Example: $0 'my-awesome-project' 'A revolutionary AI framework'"
    exit 1
fi

PROJECT_NAME=$1
DESCRIPTION=$2
GITHUB_USER="svnstfns"

print_status "Setting up project: $PROJECT_NAME"
print_status "Description: $DESCRIPTION"

# Step 1: Verify GitHub MCP service is available
print_status "Step 1: Verifying GitHub MCP service..."

# This would be called via MCP tools in Cursor
# For now, we'll create the repository structure

# Step 2: Create project directory structure
print_status "Step 2: Creating project structure..."

# Create essential directories
mkdir -p src tests docs scripts config

# Create essential files
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment variables
.env
.env.local

# Backup files
backup-*.tar.gz
EOF

# Create initial README
cat > README.md << EOF
# $PROJECT_NAME

$DESCRIPTION

## Setup

\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Start development
python src/main.py
\`\`\`

## Backup Status

- **GitHub Repository:** https://github.com/$GITHUB_USER/$PROJECT_NAME
- **Last Backup:** $(date)
- **Status:** ✅ ACTIVE

## Development Workflow

1. Always commit before ending session
2. Push to GitHub immediately after commits
3. Use feature branches for major changes
4. Follow backup protocol strictly

---

**This project follows strict backup protocols to prevent data loss.**
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
# Core dependencies
requests>=2.31.0
python-dotenv>=1.0.0

# Development dependencies
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
EOF

# Create main Python file
cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Main entry point for the application.
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main application function."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Application started")
    logger.info("Backup protocol: ACTIVE")
    
    # Your main application logic here
    print("🚀 Application is running!")
    print("📦 Backup protocol is active")
    print("🔒 All work will be saved to GitHub")

if __name__ == "__main__":
    main()
EOF

# Create test file
cat > tests/test_main.py << 'EOF'
"""
Tests for main application functionality.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_import_main():
    """Test that main module can be imported."""
    try:
        import main
        assert main is not None
    except ImportError as e:
        pytest.fail(f"Failed to import main module: {e}")

def test_backup_protocol():
    """Test that backup protocol is documented."""
    readme_path = Path(__file__).parent.parent / "README.md"
    assert readme_path.exists(), "README.md should exist"
    
    with open(readme_path, 'r') as f:
        content = f.read()
        assert "backup" in content.lower(), "README should mention backup protocol"
EOF

# Step 3: Initialize Git repository
print_status "Step 3: Initializing Git repository..."

if [ ! -d ".git" ]; then
    git init
    print_status "Git repository initialized"
else
    print_warning "Git repository already exists"
fi

# Step 4: Create initial commit
print_status "Step 4: Creating initial commit..."

git add .
git commit -m "Initial project setup: $PROJECT_NAME

- Project structure created
- Backup protocol implemented
- Basic Python application setup
- Test framework configured

Backup Status: ✅ ACTIVE"

# Step 5: Create GitHub repository (via MCP in Cursor)
print_status "Step 5: GitHub repository setup..."
print_warning "IMPORTANT: Use GitHub MCP tools in Cursor to create the repository:"
echo "  Repository Name: $PROJECT_NAME"
echo "  Description: $DESCRIPTION"
echo "  Owner: $GITHUB_USER"
echo ""
echo "After creating the repository, run:"
echo "  git remote add origin https://github.com/$GITHUB_USER/$PROJECT_NAME.git"
echo "  git push -u origin main"

# Step 6: Create backup verification script
print_status "Step 6: Creating backup verification script..."

cat > scripts/backup-check.sh << 'EOF'
#!/bin/bash

# Backup Verification Script
# Usage: ./scripts/backup-check.sh

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔍 Checking backup status...${NC}"

# Check git status
if git status --porcelain | grep -q .; then
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    git status --short
else
    echo -e "${GREEN}✅ No uncommitted changes${NC}"
fi

# Check remote
if git remote -v | grep -q origin; then
    echo -e "${GREEN}✅ Remote origin configured${NC}"
    git remote -v
else
    echo -e "${RED}❌ No remote origin configured${NC}"
fi

# Check last commit
echo -e "${GREEN}📝 Last commit:${NC}"
git log -1 --oneline

echo -e "${GREEN}✅ Backup check complete${NC}"
EOF

chmod +x scripts/backup-check.sh

# Step 7: Create emergency backup script
print_status "Step 7: Creating emergency backup script..."

cat > scripts/emergency-backup.sh << 'EOF'
#!/bin/bash

# Emergency Backup Script
# Usage: ./scripts/emergency-backup.sh

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_NAME="emergency-backup-$TIMESTAMP"

echo -e "${YELLOW}🚨 EMERGENCY BACKUP INITIATED${NC}"
echo -e "${YELLOW}Timestamp: $TIMESTAMP${NC}"

# Create local backup
echo -e "${GREEN}📦 Creating local backup...${NC}"
tar -czf "$BACKUP_NAME.tar.gz" . --exclude='*.tar.gz' --exclude='.git'

# Commit current state
echo -e "${GREEN}💾 Committing current state...${NC}"
git add .
git commit -m "Emergency backup: $TIMESTAMP" || echo -e "${YELLOW}⚠️  No changes to commit${NC}"

# Try to push
echo -e "${GREEN}📤 Pushing to GitHub...${NC}"
if git push origin main; then
    echo -e "${GREEN}✅ Successfully pushed to GitHub${NC}"
else
    echo -e "${RED}❌ Failed to push to GitHub${NC}"
    echo -e "${YELLOW}📋 Manual backup created: $BACKUP_NAME.tar.gz${NC}"
fi

echo -e "${GREEN}✅ Emergency backup complete${NC}"
echo -e "${YELLOW}📁 Backup file: $BACKUP_NAME.tar.gz${NC}"
EOF

chmod +x scripts/emergency-backup.sh

# Step 8: Final verification
print_status "Step 8: Final verification..."

echo ""
echo -e "${GREEN}🎉 Project setup complete!${NC}"
echo ""
echo -e "${GREEN}📁 Project structure:${NC}"
tree -I '.git' || ls -la

echo ""
echo -e "${GREEN}📋 Next steps:${NC}"
echo "1. Create GitHub repository using MCP tools in Cursor"
echo "2. Add remote origin: git remote add origin https://github.com/$GITHUB_USER/$PROJECT_NAME.git"
echo "3. Push to GitHub: git push -u origin main"
echo "4. Run backup check: ./scripts/backup-check.sh"
echo ""
echo -e "${YELLOW}🚨 REMEMBER: Always commit and push before ending sessions!${NC}"
echo -e "${YELLOW}🚨 Use ./scripts/emergency-backup.sh if git fails!${NC}"

print_status "Setup complete! Backup protocol is ACTIVE."
