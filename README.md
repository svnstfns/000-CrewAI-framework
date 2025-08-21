# CrewAI Framework Project

## 🚨 CRITICAL: Backup Strategy & Workflow

### Mandatory GitHub Backup Protocol

**NEVER LOSE WORK AGAIN** - This project implements a strict backup protocol to prevent data loss.

### Pre-Project Setup Checklist

Before starting ANY new project in this workspace:

1. ✅ **GitHub MCP Service Verification**
   - Confirm GitHub MCP service is running
   - Verify PAT token is valid and authenticated
   - Test authentication with `mcp_github_get_me`

2. ✅ **Repository Creation**
   - Create GitHub repository for the project
   - Set up proper branch structure
   - Configure repository settings

3. ✅ **Local Git Setup**
   - Initialize git repository
   - Add remote origin
   - Create initial commit

### Mandatory Workflow Rules

#### For Every Development Session:

1. **Before Starting Work:**
   ```bash
   # Verify GitHub connection
   # Check repository status
   git status
   git remote -v
   ```

2. **During Development:**
   - Commit frequently (at least every 30 minutes)
   - Use descriptive commit messages
   - Stage all relevant files

3. **Before Ending Session:**
   ```bash
   # Stage all changes
   git add .
   
   # Commit with descriptive message
   git commit -m "Session end: [brief description of work done]"
   
   # Push to GitHub
   git push origin main
   ```

4. **Emergency Backup (if git fails):**
   - Use GitHub MCP tools to create/update files directly
   - Document all changes made
   - Create backup branch if needed

### GitHub MCP Tools Available

Essential tools for backup and repository management:

- `mcp_github_create_repository` - Create new repositories
- `mcp_github_create_or_update_file` - Direct file upload/update
- `mcp_github_create_pull_request` - Create PRs for major changes
- `mcp_github_get_file_contents` - Retrieve files from GitHub
- `mcp_github_list_commits` - Check commit history
- `mcp_github_get_me` - Verify authentication

### Project Structure

```
000-CrewAI-framework/
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── backup-protocol.md       # Detailed backup procedures
├── scripts/                 # Automation scripts
│   ├── setup-project.sh     # Project initialization
│   ├── backup-check.sh      # Backup verification
│   └── emergency-backup.sh  # Emergency backup procedures
└── docs/                    # Project documentation
    └── workflow.md          # Development workflow
```

### Authentication Status

- **GitHub User:** svnstfns
- **Authentication:** ✅ VERIFIED
- **MCP Service:** ✅ ACTIVE
- **Last Verified:** $(date)

### Emergency Contacts

If GitHub MCP fails:
1. Use local git commands
2. Manual file upload via GitHub web interface
3. Create backup in alternative location

---

**Remember: Every line of code is precious. Backup early, backup often, backup to GitHub.**
