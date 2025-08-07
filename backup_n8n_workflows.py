#!/usr/bin/env python3
"""
n8n Workflow Backup Script
==========================

This script backs up all workflows from your n8n instance to local JSON files.
It uses the n8n API to export workflows and saves them with timestamps.

Usage:
    python3 backup_n8n_workflows.py

Requirements:
    pip install requests
"""

import os
import json
import requests
import datetime
from pathlib import Path

# n8n instance configuration
N8N_BASE_URL = "https://n8n.srv850639.hstgr.cloud"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3YmNkMjgzYy05NTg3LTQ2YjAtYjA3OC05MWYzMjE3ZTA2YjciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU0NTM1MjIxfQ.mSarTF2U6mroE5EeJmrGhWm0grLPeqHSx8O-Q2mfQ5E"

def create_backup_directory():
    """Create timestamped backup directory"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"n8n-backups/backup_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir

def get_workflows():
    """Fetch all workflows from n8n instance"""
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{N8N_BASE_URL}/api/v1/workflows"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching workflows: {e}")
        return None

def get_workflow_details(workflow_id):
    """Fetch detailed workflow data including nodes and connections"""
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{N8N_BASE_URL}/api/v1/workflows/{workflow_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching workflow {workflow_id}: {e}")
        return None

def backup_workflows():
    """Main backup function"""
    print("🔄 Starting n8n Workflow Backup")
    print("=" * 50)
    
    # Create backup directory
    backup_dir = create_backup_directory()
    print(f"📁 Backup directory: {backup_dir}")
    
    # Get all workflows
    workflows_list = get_workflows()
    if not workflows_list:
        print("❌ Failed to fetch workflows list")
        return
    
    workflows = workflows_list.get('data', [])
    print(f"📋 Found {len(workflows)} workflows to backup")
    
    # Backup each workflow
    backed_up = 0
    for workflow in workflows:
        workflow_id = workflow.get('id')
        workflow_name = workflow.get('name', f'workflow_{workflow_id}')
        
        print(f"📥 Backing up: {workflow_name} (ID: {workflow_id})")
        
        # Get detailed workflow data
        workflow_details = get_workflow_details(workflow_id)
        if workflow_details:
            # Clean filename for saving
            safe_filename = "".join(c for c in workflow_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_filename = safe_filename.replace(' ', '_')
            
            # Save workflow to file
            filename = f"{safe_filename}_{workflow_id}.json"
            filepath = backup_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(workflow_details.get('data', workflow_details), f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved: {filename}")
            backed_up += 1
        else:
            print(f"❌ Failed to backup: {workflow_name}")
    
    # Create backup summary
    summary = {
        "backup_timestamp": datetime.datetime.now().isoformat(),
        "n8n_instance": N8N_BASE_URL,
        "total_workflows": len(workflows),
        "backed_up_workflows": backed_up,
        "workflows": [
            {
                "id": w.get('id'),
                "name": w.get('name'),
                "active": w.get('active'),
                "created_at": w.get('createdAt'),
                "updated_at": w.get('updatedAt')
            }
            for w in workflows
        ]
    }
    
    # Save summary
    summary_file = backup_dir / "backup_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"🎉 Backup Complete!")
    print(f"📊 Summary:")
    print(f"   • Total workflows: {len(workflows)}")
    print(f"   • Successfully backed up: {backed_up}")
    print(f"   • Backup location: {backup_dir}")
    print(f"   • Summary file: {summary_file}")
    
    # Create latest backup symlink for easy access
    latest_link = Path("n8n-backups/latest")
    if latest_link.exists() or latest_link.is_symlink():
        latest_link.unlink()
    latest_link.symlink_to(backup_dir.name)
    print(f"   • Latest backup link: {latest_link}")

if __name__ == "__main__":
    backup_workflows()