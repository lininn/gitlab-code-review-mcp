import os
import requests
import json
from dotenv import load_dotenv
from urllib.parse import quote

# Load environment variables
load_dotenv()

# Get configuration from environment
GITLAB_HOST = os.getenv("GITLAB_HOST", "gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
API_VERSION = os.getenv("GITLAB_API_VERSION", "v4")

if not GITLAB_TOKEN:
    print("Error: GITLAB_TOKEN not set in environment")
    exit(1)

# Remove https:// prefix if present for API calls
if GITLAB_HOST.startswith("https://"):
    GITLAB_HOST = GITLAB_HOST.replace("https://", "")
elif GITLAB_HOST.startswith("http://"):
    GITLAB_HOST = GITLAB_HOST.replace("http://", "")

headers = {
    'Accept': 'application/json',
    'User-Agent': 'GitLabMRReview/1.0',
    'Private-Token': GITLAB_TOKEN
}

def make_request(url):
    """Make API request and handle response"""
    try:
        response = requests.get(url, headers=headers, verify=True, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Status code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return None

def fetch_merge_request_details(project_id, mr_iid):
    """Fetch complete details for a merge request"""
    print(f"Fetching details for merge request #{mr_iid} in project {project_id}")
    
    # Get merge request basic info
    mr_endpoint = f"https://{GITLAB_HOST}/api/{API_VERSION}/projects/{quote(project_id, safe='')}/merge_requests/{mr_iid}"
    mr_info = make_request(mr_endpoint)
    
    if not mr_info:
        print("Failed to get merge request info")
        return None
    
    # Get changes/diffs
    changes_endpoint = f"{mr_endpoint}/changes"
    changes_info = make_request(changes_endpoint)
    
    # Get commits
    commits_endpoint = f"{mr_endpoint}/commits"
    commits_info = make_request(commits_endpoint)
    
    # Get notes/comments
    notes_endpoint = f"{mr_endpoint}/notes"
    notes_info = make_request(notes_endpoint)
    
    return {
        "merge_request": mr_info,
        "changes": changes_info,
        "commits": commits_info,
        "notes": notes_info
    }

def print_mr_summary(mr_data):
    """Print a summary of the merge request"""
    if not mr_data:
        return
    
    mr_info = mr_data["merge_request"]
    changes = mr_data["changes"]
    commits = mr_data["commits"]
    notes = mr_data["notes"]
    
    print("\n" + "="*80)
    print("MERGE REQUEST SUMMARY")
    print("="*80)
    print(f"Title: {mr_info.get('title', 'No title')}")
    print(f"Author: {mr_info.get('author', {}).get('name', 'Unknown')}")
    print(f"State: {mr_info.get('state', 'Unknown')}")
    print(f"Created: {mr_info.get('created_at', 'Unknown')}")
    print(f"Updated: {mr_info.get('updated_at', 'Unknown')}")
    print(f"Source branch: {mr_info.get('source_branch', 'Unknown')}")
    print(f"Target branch: {mr_info.get('target_branch', 'Unknown')}")
    print(f"Merge status: {mr_info.get('merge_status', 'Unknown')}")
    
    print(f"\nChanges: {len(changes.get('changes', [])) if changes else 0} files changed")
    print(f"Commits: {len(commits) if commits else 0} commits")
    print(f"Comments: {len(notes) if notes else 0} notes")
    
    # Print changed files
    if changes and 'changes' in changes:
        print(f"\nChanged files:")
        for change in changes['changes']:
            old_path = change.get('old_path', 'N/A')
            new_path = change.get('new_path', 'N/A')
            diff = change.get('diff', '')
            lines_added = diff.count('\n+') - diff.count('\n+++')
            lines_removed = diff.count('\n-') - diff.count('\n---')
            
            print(f"  - {new_path} ({old_path})")
            print(f"    +{lines_added} -{lines_removed} lines")

# Main execution
if __name__ == "__main__":
    project_id = "front-end/wmflight"
    mr_iid = "924"
    
    mr_data = fetch_merge_request_details(project_id, mr_iid)
    
    if mr_data:
        print_mr_summary(mr_data)
        
        # Save detailed data to file for analysis
        with open(f"mr_{mr_iid}_details.json", "w", encoding="utf-8") as f:
            json.dump(mr_data, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed data saved to mr_{mr_iid}_details.json")
    else:
        print("Failed to fetch merge request data")