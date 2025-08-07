#!/usr/bin/env python3
"""
n8n Workflow Restore Script
===========================

This script restores workflows from backup JSON files to your n8n instance.
It can restore individual workflows or entire backup directories.

Usage:
    # Restore from latest backup
    python3 restore_n8n_workflows.py --latest
    
    # Restore from specific backup directory
    python3 restore_n8n_workflows.py --backup-dir n8n-backups/backup_20250107_123456
    
    # Restore specific workflow file
    python3 restore_n8n_workflows.py --file workflow_file.json

Requirements:
    pip install requests
"""

import os
import json
import requests
import argparse
from pathlib import Path

# n8n instance configuration
N8N_BASE_URL = "https://n8n.srv850639.hstgr.cloud"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3YmNkMjgzYy05NTg3LTQ2YjAtYjA3OC05MWYzMjE3ZTA2YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU0NTM1MjIxfQ.mSarTF2U6mroE5EeJmrGhWm0grLPeqHSx8O-Q2mfQ5E"

def create_workflow(workflow_data):
    """Create a new workflow in n8n"""
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{N8N_BASE_URL}/api/v1/workflows"
    
    try:
        response = requests.post(url, headers=headers, json=workflow_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating workflow: {e}")
        return None

def update_workflow(workflow_id, workflow_data):
    """Update an existing workflow in n8n"""
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{N8N_BASE_URL}/api/v1/workflows/{workflow_id}"
    
    try:
        response = requests.put(url, headers=headers, json=workflow_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating workflow {workflow_id}: {e}")
        return None

def get_existing_workflows():
    """Get list of existing workflows"""
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{N8N_BASE_URL}/api/v1/workflows"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        workflows = response.json().get('data', [])
        return {w['name']: w['id'] for w in workflows}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching existing workflows: {e}")
        return {}

def restore_workflow_file(filepath, existing_workflows):
    """Restore a single workflow file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        
        workflow_name = workflow_data.get('name', 'Unknown Workflow')
        print(f"📥 Restoring: {workflow_name}")
        
        # Check if workflow already exists
        if workflow_name in existing_workflows:
            print(f"⚠️  Workflow '{workflow_name}' already exists. Updating...")
            result = update_workflow(existing_workflows[workflow_name], workflow_data)
        else:
            print(f"➕ Creating new workflow: {workflow_name}")
            result = create_workflow(workflow_data)
        
        if result:
            print(f"✅ Successfully restored: {workflow_name}")
            return True
        else:
            print(f"❌ Failed to restore: {workflow_name}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def restore_from_directory(backup_dir):
    """Restore all workflows from a backup directory"""
    backup_path = Path(backup_dir)
    if not backup_path.exists():
        print(f"❌ Backup directory not found: {backup_dir}")
        return
    
    # Find all JSON workflow files (exclude summary)
    workflow_files = [f for f in backup_path.glob("*.json") if f.name != "backup_summary.json"]
    
    if not workflow_files:
        print(f"❌ No workflow files found in {backup_dir}")
        return
    
    print(f"📁 Restoring from: {backup_dir}")
    print(f"📋 Found {len(workflow_files)} workflow files")
    
    # Get existing workflows to avoid duplicates
    existing_workflows = get_existing_workflows()
    
    # Restore each workflow
    restored = 0
    for workflow_file in workflow_files:
        if restore_workflow_file(workflow_file, existing_workflows):
            restored += 1
    
    print(f"\n🎉 Restore Complete!")
    print(f"📊 Summary: {restored}/{len(workflow_files)} workflows restored successfully")

def main():
    parser = argparse.ArgumentParser(description="Restore n8n workflows from backup")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--latest", action="store_true", help="Restore from latest backup")
    group.add_argument("--backup-dir", help="Restore from specific backup directory")
    group.add_argument("--file", help="Restore specific workflow file")
    
    args = parser.parse_args()
    
    print("🔄 Starting n8n Workflow Restore")
    print("=" * 50)
    
    if args.latest:
        latest_link = Path("n8n-backups/latest")
        if latest_link.exists():
            backup_dir = latest_link.resolve()
            restore_from_directory(backup_dir)
        else:
            print("❌ No latest backup found. Run backup script first.")
    
    elif args.backup_dir:
        restore_from_directory(args.backup_dir)
    
    elif args.file:
        existing_workflows = get_existing_workflows()
        restore_workflow_file(Path(args.file), existing_workflows)

if __name__ == "__main__":
    main()