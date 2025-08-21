# MANDATORY GITHUB BACKUP RULES - ALL WORKSPACES

## 🚨 CRITICAL: NO WORK WITHOUT GITHUB BACKUP

**RULE #1: If GitHub backup fails, work stops immediately.**

---

## PRE-WORK VERIFICATION (MANDATORY BEFORE ANY CODING)

### 1. GitHub MCP Service Authentication
- **REQUIRED**: Verify GitHub MCP service is running
- **REQUIRED**: Confirm PAT Token is valid and authenticated
- **REQUIRED**: Test authentication with a simple API call
- **FAILURE**: If any step fails, STOP ALL WORK until resolved

### 2. Repository Setup Verification
- **REQUIRED**: Check if remote repository exists
- **REQUIRED**: If not exists → CREATE remote repository
- **REQUIRED**: Link local workspace to remote repository
- **REQUIRED**: Verify remote connection is working
- **FAILURE**: If any step fails, STOP ALL WORK until resolved

---

## DURING WORK SESSIONS

### 3. Continuous Backup Protocol
- **EVERY 15 MINUTES**: Stage all changes (`git add .`)
- **EVERY 15 MINUTES**: Commit with descriptive message
- **EVERY 15 MINUTES**: Push to remote repository
- **EVERY 15 MINUTES**: Verify push was successful
- **FAILURE**: If push fails, STOP ALL WORK until resolved

### 4. File Content Verification
- **REQUIRED**: Verify ALL files are tracked by git
- **REQUIRED**: Verify ALL file content is complete (no truncation)
- **REQUIRED**: Verify ALL folders are properly committed
- **REQUIRED**: Check file sizes match local vs remote
- **FAILURE**: If any verification fails, STOP ALL WORK until resolved

---

## END-OF-SESSION MANDATORY CHECKS

### 5. Final Backup Verification
- **REQUIRED**: Complete `git status` check (must be clean)
- **REQUIRED**: Force push to ensure remote is current
- **REQUIRED**: Verify all files are on GitHub
- **REQUIRED**: Test repository clone to verify backup integrity
- **FAILURE**: If any check fails, DO NOT CLOSE CURSOR until resolved

---

## EMERGENCY PROTOCOLS

### 6. Network/Service Failures
- **IF**: GitHub is down, network fails, or PAT expires
- **THEN**: IMMEDIATELY STOP ALL CODING
- **THEN**: Save all work locally (if possible)
- **THEN**: Wait for service restoration
- **THEN**: Resume only after successful backup verification

### 7. Payment/Subscription Issues
- **IF**: GitHub subscription lapsed or payment issues
- **THEN**: IMMEDIATELY STOP ALL CODING
- **THEN**: Resolve payment/subscription issues
- **THEN**: Resume only after successful backup verification

---

## TOOL USAGE RESTRICTIONS

### 8. Required GitHub MCP Tools Only
**ALLOWED TOOLS:**
- `mcp_github_get_me` - Verify authentication
- `mcp_github_create_repository` - Create remote repos
- `mcp_github_create_or_update_file` - Backup files
- `mcp_github_get_file_contents` - Verify backups
- `mcp_github_list_branches` - Check repository status
- `mcp_github_create_branch` - Create backup branches
- `mcp_github_create_commit` - Commit changes
- `mcp_github_push` - Push to remote

**BLOCKED TOOLS:** All other tools until backup is verified

---

## VERIFICATION CHECKLIST

### 9. Daily Startup Checklist
- [ ] GitHub MCP service running
- [ ] PAT Token valid and authenticated
- [ ] Remote repository exists and linked
- [ ] Local workspace clean (no uncommitted changes)
- [ ] Remote repository accessible
- [ ] All previous work verified on GitHub

### 10. Every 15 Minutes Checklist
- [ ] All changes staged
- [ ] All changes committed
- [ ] All changes pushed to remote
- [ ] Push verification successful
- [ ] No error messages

### 11. End-of-Session Checklist
- [ ] All files committed and pushed
- [ ] Git status clean
- [ ] Remote repository current
- [ ] Backup integrity verified
- [ ] Ready to close Cursor safely

---

## ENFORCEMENT

### 12. Zero Tolerance Policy
- **NO EXCEPTIONS** to these rules
- **NO "JUST ONE MORE CHANGE"** without backup
- **NO WORK** without GitHub backup working
- **NO CURSOR CLOSURE** without backup verification

### 13. Failure Consequences
- **IF** backup fails → STOP ALL WORK
- **IF** verification fails → STOP ALL WORK  
- **IF** network fails → STOP ALL WORK
- **IF** GitHub down → STOP ALL WORK
- **WORK RESUMES ONLY** after successful backup restoration

---

## RECOVERY PROCEDURES

### 14. Lost Work Recovery
- **IF** work is lost due to backup failure
- **THEN** this is a CRITICAL FAILURE
- **THEN** review and strengthen backup procedures
- **THEN** implement additional safety measures
- **THEN** NEVER repeat the same failure

---

## REMINDER

**THESE RULES ARE MANDATORY FOR ALL WORKSPACES**
**THESE RULES PREVENT WORK LOSS**
**THESE RULES ARE NON-NEGOTIABLE**
**FOLLOW THEM OR LOSE WORK FOREVER**

---

*Last Updated: [Current Date]*
*Applicable to: ALL Cursor Workspaces*
*Enforcement: IMMEDIATE AND PERMANENT*
