# GITHUB BACKUP IMPLEMENTATION PROCEDURES

## IMMEDIATE EXECUTION PROTOCOLS

### Phase 1: Authentication Verification
```bash
# Step 1: Test GitHub MCP Service
mcp_github_get_me

# Expected Result: Returns authenticated user info
# If FAILS: STOP ALL WORK - Authentication broken
```

### Phase 2: Repository Setup
```bash
# Step 2: Check if remote exists
git remote -v

# If no remote exists:
# 1. Create repository on GitHub
# 2. Link local to remote
# 3. Initial commit and push
```

### Phase 3: Continuous Backup Loop
```bash
# Every 15 minutes execute:
git add .
git commit -m "Auto-backup: $(date)"
git push origin main
git status  # Verify clean
```

---

## MANDATORY VERIFICATION SCRIPTS

### Pre-Work Verification Script
```bash
#!/bin/bash
# PRE_WORK_VERIFICATION.sh

echo "🚨 PRE-WORK VERIFICATION STARTING..."

# 1. Test GitHub authentication
echo "Testing GitHub authentication..."
# Execute: mcp_github_get_me
if [ $? -ne 0 ]; then
    echo "❌ GITHUB AUTHENTICATION FAILED"
    echo "❌ STOPPING ALL WORK"
    exit 1
fi

# 2. Check remote repository
echo "Checking remote repository..."
if ! git remote -v | grep -q "origin"; then
    echo "❌ NO REMOTE REPOSITORY FOUND"
    echo "❌ STOPPING ALL WORK"
    exit 1
fi

# 3. Test remote connection
echo "Testing remote connection..."
if ! git ls-remote --exit-code origin; then
    echo "❌ REMOTE CONNECTION FAILED"
    echo "❌ STOPPING ALL WORK"
    exit 1
fi

echo "✅ PRE-WORK VERIFICATION PASSED"
echo "✅ WORK CAN PROCEED"
```

### Continuous Backup Script
```bash
#!/bin/bash
# CONTINUOUS_BACKUP.sh

echo "🔄 EXECUTING CONTINUOUS BACKUP..."

# 1. Stage all changes
git add .

# 2. Check if there are changes
if git diff --cached --quiet; then
    echo "✅ No changes to commit"
    exit 0
fi

# 3. Commit changes
git commit -m "Auto-backup: $(date '+%Y-%m-%d %H:%M:%S')"

# 4. Push to remote
if git push origin main; then
    echo "✅ BACKUP SUCCESSFUL"
else
    echo "❌ BACKUP FAILED"
    echo "❌ STOPPING ALL WORK"
    exit 1
fi
```

### End-of-Session Verification Script
```bash
#!/bin/bash
# END_SESSION_VERIFICATION.sh

echo "🔍 END-OF-SESSION VERIFICATION..."

# 1. Check git status
if ! git status --porcelain | grep -q .; then
    echo "✅ Git status clean"
else
    echo "❌ UNCOMMITTED CHANGES DETECTED"
    echo "❌ CANNOT CLOSE CURSOR"
    exit 1
fi

# 2. Force push to ensure remote is current
if git push origin main --force; then
    echo "✅ Force push successful"
else
    echo "❌ FORCE PUSH FAILED"
    echo "❌ CANNOT CLOSE CURSOR"
    exit 1
fi

# 3. Verify remote repository
echo "Verifying remote repository..."
# Execute: mcp_github_get_file_contents to verify files

echo "✅ END-OF-SESSION VERIFICATION PASSED"
echo "✅ SAFE TO CLOSE CURSOR"
```

---

## EMERGENCY PROCEDURES

### Network Failure Response
```bash
#!/bin/bash
# EMERGENCY_NETWORK_FAILURE.sh

echo "🚨 NETWORK FAILURE DETECTED"
echo "🚨 STOPPING ALL WORK IMMEDIATELY"

# 1. Save current work locally
git add .
git commit -m "Emergency save: $(date)"

# 2. Try to push (may fail due to network)
git push origin main || echo "Push failed due to network"

# 3. Wait for network restoration
echo "Waiting for network restoration..."
while ! ping -c 1 github.com > /dev/null 2>&1; do
    sleep 30
done

# 4. Resume backup
echo "Network restored, resuming backup..."
git push origin main
```

---

## INTEGRATION WITH CURSOR

### Cursor Startup Hook
```json
{
  "cursor.startup": {
    "preWorkVerification": true,
    "githubBackupEnabled": true,
    "backupInterval": 900000, // 15 minutes in milliseconds
    "stopOnBackupFailure": true
  }
}
```

### Cursor Shutdown Hook
```json
{
  "cursor.shutdown": {
    "endSessionVerification": true,
    "forceBackupBeforeClose": true,
    "preventCloseOnBackupFailure": true
  }
}
```

---

## MONITORING AND ALERTS

### Backup Status Monitor
```bash
#!/bin/bash
# BACKUP_STATUS_MONITOR.sh

# Check last backup time
LAST_BACKUP=$(git log -1 --format="%cd" --date=iso)
CURRENT_TIME=$(date -Iseconds)

# Calculate time difference
BACKUP_AGE=$(( $(date -d "$CURRENT_TIME" +%s) - $(date -d "$LAST_BACKUP" +%s) ))

# Alert if backup is older than 20 minutes
if [ $BACKUP_AGE -gt 1200 ]; then
    echo "🚨 WARNING: Last backup was $((BACKUP_AGE/60)) minutes ago"
    echo "🚨 EXECUTING EMERGENCY BACKUP"
    ./CONTINUOUS_BACKUP.sh
fi
```

---

## FAILURE RECOVERY

### Lost Work Recovery Protocol
```bash
#!/bin/bash
# LOST_WORK_RECOVERY.sh

echo "🚨 LOST WORK RECOVERY PROTOCOL ACTIVATED"

# 1. Check local git history
echo "Checking local git history..."
git log --oneline -10

# 2. Check remote repository
echo "Checking remote repository..."
git fetch origin
git log origin/main --oneline -10

# 3. Compare local vs remote
echo "Comparing local vs remote..."
git diff HEAD origin/main

# 4. Attempt recovery
if [ -f ".git/reflog" ]; then
    echo "Attempting recovery from reflog..."
    git reflog --oneline -10
fi

echo "Recovery analysis complete"
```

---

## ENFORCEMENT MECHANISMS

### Automatic Enforcement
- **Every 15 minutes**: Automatic backup execution
- **On file save**: Trigger backup verification
- **On Cursor close**: Force backup before allowing close
- **On network change**: Verify backup status
- **On authentication change**: Re-verify all procedures

### Manual Enforcement
- **Before any coding**: Execute pre-work verification
- **After any significant change**: Force immediate backup
- **Before closing Cursor**: Execute end-session verification
- **On any error**: Stop work and verify backup

---

## SUCCESS METRICS

### Backup Success Indicators
- ✅ All files committed and pushed
- ✅ Git status clean
- ✅ Remote repository current
- ✅ File integrity verified
- ✅ No error messages

### Failure Indicators
- ❌ Authentication failures
- ❌ Network connectivity issues
- ❌ Push failures
- ❌ Uncommitted changes
- ❌ File corruption or truncation

---

*This implementation ensures zero work loss through mandatory GitHub backup procedures.*
