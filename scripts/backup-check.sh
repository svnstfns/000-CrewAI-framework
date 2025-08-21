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

# Check if we can reach GitHub
echo -e "${GREEN}🌐 Testing GitHub connection...${NC}"
if curl -s --head https://github.com/svnstfns/000-CrewAI-framework | head -n 1 | grep "HTTP/1.[01] [23].." > /dev/null; then
    echo -e "${GREEN}✅ GitHub repository accessible${NC}"
else
    echo -e "${YELLOW}⚠️  GitHub repository may not be accessible${NC}"
fi

echo -e "${GREEN}✅ Backup check complete${NC}"
