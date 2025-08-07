# n8n Workflow Backup & Restore Guide

## Overview

This guide provides comprehensive backup and restore solutions for your n8n workflows running at `https://n8n.srv850639.hstgr.cloud/`.

## Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Backup All Workflows

```bash
python3 backup_n8n_workflows.py
```

### 3. Restore from Latest Backup

```bash
python3 restore_n8n_workflows.py --latest
```

## Backup Features

### Automated Backup Script (`backup_n8n_workflows.py`)

✅ **Connects to your n8n instance using API key**  
✅ **Downloads all workflows with full configuration**  
✅ **Creates timestamped backup directories**  
✅ **Saves individual JSON files for each workflow**  
✅ **Generates backup summary with metadata**  
✅ **Creates 'latest' symlink for easy access**  

### What Gets Backed Up

- **Complete workflow definitions** (nodes, connections, settings)
- **Workflow metadata** (name, ID, creation date, active status)
- **Node configurations** (credentials references, parameters)
- **Webhook configurations** (triggers, paths, methods)
- **Environment variables** (where applicable)

## Backup Directory Structure

```
n8n-backups/
├── latest -> backup_20250107_143022/
├── backup_20250107_143022/
│   ├── AI_Trading_Signal_Processor_1.json
│   ├── Trading_Bot_Alerts_2.json
│   ├── Portfolio_Monitor_3.json
│   └── backup_summary.json
└── backup_20250107_120000/
    ├── ...
    └── backup_summary.json
```

## Restore Options

### Option 1: Restore Latest Backup

```bash
python3 restore_n8n_workflows.py --latest
```

### Option 2: Restore Specific Backup

```bash
python3 restore_n8n_workflows.py --backup-dir n8n-backups/backup_20250107_143022
```

### Option 3: Restore Individual Workflow

```bash
python3 restore_n8n_workflows.py --file n8n-backups/latest/Trading_Bot_Alerts_2.json
```

## Manual Backup Methods

### Method 1: Export via n8n UI

1. **Open n8n Dashboard**: `https://n8n.srv850639.hstgr.cloud/`
2. **Navigate to workflow**
3. **Click Settings → Download**
4. **Save JSON file**

### Method 2: API Export

```bash
# Get all workflows
curl -H "X-N8N-API-KEY: YOUR_API_KEY" \
     https://n8n.srv850639.hstgr.cloud/api/v1/workflows

# Export specific workflow
curl -H "X-N8N-API-KEY: YOUR_API_KEY" \
     https://n8n.srv850639.hstgr.cloud/api/v1/workflows/WORKFLOW_ID
```

## Backup Best Practices

### 1. Regular Automated Backups

Set up a cron job for daily backups:

```bash
# Add to crontab (crontab -e)
0 2 * * * cd /path/to/trading-bot && python3 backup_n8n_workflows.py
```

### 2. Version Control Integration

```bash
# Add backups to git (optional)
git add n8n-backups/
git commit -m "n8n workflow backup $(date)"
git push origin main
```

### 3. Cloud Storage Sync

```bash
# Sync to cloud storage (example with rclone)
rclone sync n8n-backups/ dropbox:trading-bot-backups/n8n/
```

## Security Considerations

### API Key Protection

- **Never commit API keys to version control**
- **Use environment variables for production**
- **Rotate API keys regularly**

```bash
# Use environment variable instead
export N8N_API_KEY="your-api-key-here"
```

### Credential Handling

- **Workflows export credential references, not actual values**
- **Credentials must be manually recreated after restore**
- **Document credential mappings separately**

## Troubleshooting

### Common Issues

#### 1. API Connection Failed

```
Error fetching workflows: ConnectionError
```

**Solutions**:
- Check n8n instance is running: `https://n8n.srv850639.hstgr.cloud/`
- Verify API key is valid
- Check network connectivity

#### 2. Permission Denied

```
Error: 401 Unauthorized
```

**Solutions**:
- Regenerate API key in n8n Settings
- Update API key in script
- Check API key format

#### 3. Workflow Import Failed

```
Error creating workflow: 400 Bad Request
```

**Solutions**:
- Check workflow JSON syntax
- Verify node types are available
- Update node versions if needed

### Debug Mode

Run scripts with verbose output:

```bash
python3 backup_n8n_workflows.py --debug
python3 restore_n8n_workflows.py --latest --debug
```

## Advanced Usage

### Custom Backup Locations

Modify script variables:

```python
# In backup_n8n_workflows.py
BACKUP_BASE_DIR = "/custom/backup/path"
```

### Selective Backup

Filter workflows by criteria:

```python
# Backup only active workflows
workflows = [w for w in workflows if w.get('active', False)]
```

### Backup Scheduling

#### Daily Backup Script

```bash
#!/bin/bash
# backup_daily.sh

cd /opt/trading-bot
python3 backup_n8n_workflows.py

# Keep only last 30 days
find n8n-backups/ -name "backup_*" -type d -mtime +30 -exec rm -rf {} \;

echo "Daily n8n backup completed: $(date)"
```

#### Weekly Full Backup

```bash
#!/bin/bash
# backup_weekly.sh

cd /opt/trading-bot
python3 backup_n8n_workflows.py

# Create weekly archive
tar -czf "n8n-weekly-backup-$(date +%Y%m%d).tar.gz" n8n-backups/latest/

echo "Weekly n8n backup archived: $(date)"
```

## Recovery Scenarios

### Scenario 1: Workflow Corruption

```bash
# Stop corrupted workflow
# Restore from backup
python3 restore_n8n_workflows.py --file n8n-backups/latest/workflow_name.json
```

### Scenario 2: Complete n8n Reset

```bash
# Backup everything first
python3 backup_n8n_workflows.py

# After n8n reset/reinstall
python3 restore_n8n_workflows.py --latest
```

### Scenario 3: Migration to New Instance

```bash
# Export from old instance
python3 backup_n8n_workflows.py

# Update API URL and key for new instance
# Import to new instance
python3 restore_n8n_workflows.py --latest
```

## Monitoring & Alerts

### Backup Success Monitoring

```bash
# Add to backup script
if [ $? -eq 0 ]; then
    echo "✅ n8n backup successful: $(date)" >> /var/log/n8n-backup.log
else
    echo "❌ n8n backup failed: $(date)" >> /var/log/n8n-backup.log
    # Send alert email/notification
fi
```

This comprehensive backup solution ensures your n8n workflows are always protected and can be quickly restored when needed!