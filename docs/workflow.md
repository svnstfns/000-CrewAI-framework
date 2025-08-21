# Development Workflow - Backup-First Approach

## 🚨 MANDATORY WORKFLOW RULES

### Session Start Protocol (5 minutes)

#### 1. Environment Check
```bash
# Verify GitHub MCP service
# This is done automatically in Cursor via MCP tools

# Check local git status
git status

# Verify remote connection
git remote -v

# Pull latest changes
git pull origin main
```

#### 2. Session Branch Creation (for major features)
```bash
# Create feature branch with timestamp
git checkout -b feature/$(date +%Y%m%d-%H%M)-description

# Example: feature/20241201-1430-user-authentication
```

### During Development (Every 30 minutes)

#### 1. Quick Save
```bash
# Stage all changes
git add .

# Commit with WIP message
git commit -m "WIP: [brief description of current work]"

# Push to GitHub
git push origin $(git branch --show-current)
```

#### 2. Progress Check
- Verify files are committed
- Check GitHub repository for latest commits
- Document any issues or blockers

### Session End Protocol (MANDATORY)

#### 1. Final Commit
```bash
# Stage all remaining changes
git add .

# Create comprehensive commit message
git commit -m "Session end: [detailed description of work completed]

- Feature A implemented
- Bug B fixed
- Tests C added
- Documentation D updated

Backup Status: ✅ VERIFIED"
```

#### 2. Push to GitHub
```bash
# Push current branch
git push origin $(git branch --show-current)

# If on feature branch, merge to main
if [ "$(git branch --show-current)" != "main" ]; then
    git checkout main
    git merge $(git branch --show-current)
    git push origin main
    git branch -d $(git branch --show-current)
fi
```

#### 3. Verification
```bash
# Run backup check
./scripts/backup-check.sh

# Verify on GitHub web interface
# Check commit history
# Confirm all files are present
```

## Emergency Procedures

### If Git Commands Fail

#### 1. Use GitHub MCP Direct Upload
```python
# For each important file, use MCP tools
mcp_github_create_or_update_file(
    owner="svnstfns",
    repo="project-name",
    path="path/to/file",
    content="file content",
    message="Emergency backup: [filename]",
    branch="main"
)
```

#### 2. Create Emergency Branch
```python
mcp_github_create_branch(
    owner="svnstfns",
    repo="project-name",
    branch=f"emergency-backup-{datetime.now().strftime('%Y%m%d-%H%M')}"
)
```

### If GitHub MCP Fails

#### 1. Local Backup
```bash
# Run emergency backup script
./scripts/emergency-backup.sh

# This creates:
# - Timestamped tar.gz backup
# - Local commit
# - Attempts to push to GitHub
```

#### 2. Alternative Backup
```bash
# Copy to safe location
cp -r . ~/Desktop/backup-$(date +%Y%m%d-%H%M)

# Create archive
tar -czf ~/Desktop/backup-$(date +%Y%m%d-%H%M).tar.gz .
```

## Quality Assurance

### Code Review Checklist
- [ ] All changes are committed
- [ ] All changes are pushed to GitHub
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] Backup verification completed

### Weekly Maintenance
- [ ] Review all branches
- [ ] Clean up old feature branches
- [ ] Update backup protocol if needed
- [ ] Test recovery procedures
- [ ] Update project documentation

## Tools and Scripts

### Essential Commands
```bash
# Check backup status
./scripts/backup-check.sh

# Emergency backup
./scripts/emergency-backup.sh

# Setup new project
./scripts/setup-project.sh "project-name" "description"
```

### GitHub MCP Tools
- `mcp_github_get_me` - Verify authentication
- `mcp_github_create_repository` - Create new repository
- `mcp_github_create_or_update_file` - Direct file upload
- `mcp_github_create_branch` - Create backup branch
- `mcp_github_list_commits` - Check commit history

## Best Practices

### Commit Messages
- Use descriptive commit messages
- Include context and reasoning
- Reference issues or features
- Always mention backup status

### File Organization
- Keep related files together
- Use consistent naming conventions
- Document file purposes
- Include backup status in README

### Error Handling
- Document all errors encountered
- Create backup before troubleshooting
- Test recovery procedures
- Update protocols based on lessons learned

## Recovery Procedures

### If Work is Lost
1. Check GitHub commit history
2. Look for backup branches
3. Check local git reflog
4. Restore from emergency backups
5. Document the incident

### If Repository is Corrupted
1. Clone fresh from GitHub
2. Apply any local changes
3. Verify all files are present
4. Update backup protocols
5. Test recovery procedures

---

**This workflow is MANDATORY. Follow it religiously to prevent data loss.**
