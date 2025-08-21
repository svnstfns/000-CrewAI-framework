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
