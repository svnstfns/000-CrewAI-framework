# Backup Protocol - Never Lose Work Again

## 🚨 CRITICAL PROCEDURES

### Phase 1: Project Initialization (MANDATORY)

#### Step 1: GitHub Repository Creation
```bash
# Use GitHub MCP to create repository
mcp_github_create_repository:
  - name: "project-name"
  - description: "Project description"
  - private: true/false
  - autoInit: true
```

#### Step 2: Local Git Setup
```bash
# Initialize local repository
git init

# Add remote origin
git remote add origin https://github.com/svnstfns/project-name.git

# Create initial commit
git add .
git commit -m "Initial project setup"

# Push to GitHub
git push -u origin main
```

#### Step 3: Verification
```bash
# Verify remote connection
git remote -v

# Check GitHub repository exists
# Verify files are uploaded
```

### Phase 2: Development Session Protocol

#### Before Starting Work (5 minutes)
1. **Check GitHub Status**
   ```bash
   mcp_github_get_me  # Verify authentication
   git status         # Check local status
   git pull origin main  # Get latest changes
   ```

2. **Create Session Branch** (for major features)
   ```bash
   git checkout -b feature/session-$(date +%Y%m%d-%H%M)
   ```

#### During Development (Every 30 minutes)
1. **Stage Changes**
   ```bash
   git add .
   ```

2. **Commit with Description**
   ```bash
   git commit -m "WIP: [brief description of current work]"
   ```

3. **Push to GitHub**
   ```bash
   git push origin $(git branch --show-current)
   ```

#### End of Session (MANDATORY)
1. **Final Commit**
   ```bash
   git add .
   git commit -m "Session end: [comprehensive description of work completed]"
   ```

2. **Push to GitHub**
   ```bash
   git push origin $(git branch --show-current)
   ```

3. **Merge to Main** (if working on feature branch)
   ```bash
   git checkout main
   git merge $(git branch --show-current)
   git push origin main
   ```

### Phase 3: Emergency Backup Procedures

#### If Git Commands Fail
1. **Use GitHub MCP Direct Upload**
   ```bash
   # For each important file
   mcp_github_create_or_update_file:
     - owner: svnstfns
     - repo: project-name
     - path: "path/to/file"
     - content: "file content"
     - message: "Emergency backup: [filename]"
     - branch: main
   ```

2. **Create Backup Branch**
   ```bash
   mcp_github_create_branch:
     - owner: svnstfns
     - repo: project-name
     - branch: "emergency-backup-$(date +%Y%m%d-%H%M)"
   ```

#### If GitHub MCP Fails
1. **Local Backup**
   ```bash
   # Create timestamped backup
   cp -r . ../backup-$(date +%Y%m%d-%H%M)
   
   # Archive current state
   tar -czf backup-$(date +%Y%m%d-%H%M).tar.gz .
   ```

2. **Alternative Cloud Backup**
   - Upload to Google Drive/Dropbox
   - Use alternative Git hosting (GitLab, Bitbucket)
   - Email important files to yourself

### Phase 4: Verification Procedures

#### Daily Verification
1. **Check GitHub Repository**
   - Verify all files are present
   - Check commit history
   - Confirm no files are missing

2. **Test Repository Access**
   ```bash
   # Clone to temporary location
   git clone https://github.com/svnstfns/project-name.git /tmp/test-clone
   
   # Verify files
   ls -la /tmp/test-clone
   
   # Clean up
   rm -rf /tmp/test-clone
   ```

#### Weekly Verification
1. **Full Repository Audit**
   - Review all branches
   - Check file integrity
   - Verify backup procedures

2. **Update Documentation**
   - Update README.md
   - Review backup protocol
   - Document any issues

### Phase 5: Recovery Procedures

#### If Work is Lost
1. **Check GitHub History**
   ```bash
   mcp_github_list_commits:
     - owner: svnstfns
     - repo: project-name
   ```

2. **Recover from Last Commit**
   ```bash
   git log --oneline  # Find last good commit
   git reset --hard <commit-hash>
   ```

3. **Check All Branches**
   ```bash
   git branch -a  # List all branches
   git checkout <branch-name>  # Check each branch
   ```

### Automation Scripts

#### setup-project.sh
```bash
#!/bin/bash
# Automated project setup with backup

PROJECT_NAME=$1
DESCRIPTION=$2

# Create GitHub repository
# Initialize local git
# Set up backup procedures
# Verify everything works
```

#### backup-check.sh
```bash
#!/bin/bash
# Verify backup status

# Check git status
# Verify GitHub connection
# Test repository access
# Report any issues
```

#### emergency-backup.sh
```bash
#!/bin/bash
# Emergency backup procedures

# Create timestamped backup
# Upload to GitHub via MCP
# Create backup branch
# Document what was backed up
```

## 🚨 CRITICAL REMINDERS

1. **NEVER** work without GitHub backup
2. **ALWAYS** commit before ending session
3. **VERIFY** backup before closing Cursor
4. **DOCUMENT** any issues immediately
5. **TEST** recovery procedures regularly

## Contact Information

- **GitHub User:** svnstfns
- **Backup Protocol Version:** 1.0
- **Last Updated:** $(date)
- **Status:** ACTIVE

---

**This protocol is MANDATORY. Follow it religiously to prevent data loss.**
