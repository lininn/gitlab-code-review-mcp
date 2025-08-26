import os
import requests
from dotenv import load_dotenv

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

print(f"Testing connection to GitLab host: {GITLAB_HOST}")
print(f"Using API version: {API_VERSION}")

# Test basic API connection
url = f"https://{GITLAB_HOST}/api/{API_VERSION}/version"
headers = {
    'Accept': 'application/json',
    'User-Agent': 'GitLabConnectionTest/1.0',
    'Private-Token': GITLAB_TOKEN
}

try:
    print(f"Making request to: {url}")
    response = requests.get(url, headers=headers, verify=True, timeout=30)
    
    if response.status_code == 200:
        print("✅ Connection successful!")
        version_info = response.json()
        print(f"GitLab version: {version_info.get('version', 'Unknown')}")
        print(f"Revision: {version_info.get('revision', 'Unknown')}")
    else:
        print(f"❌ Connection failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {str(e)}")
    if hasattr(e, 'response') and e.response:
        print(f"Response status: {e.response.status_code}")
        print(f"Response text: {e.response.text}")

# Test project access
project_id = "front-end/wmflight"
project_url = f"https://{GITLAB_HOST}/api/{API_VERSION}/projects/{project_id.replace('/', '%2F')}"

print(f"\nTesting access to project: {project_id}")
print(f"Project URL: {project_url}")

try:
    response = requests.get(project_url, headers=headers, verify=True, timeout=30)
    
    if response.status_code == 200:
        project_info = response.json()
        print("✅ Project access successful!")
        print(f"Project name: {project_info.get('name', 'Unknown')}")
        print(f"Project ID: {project_info.get('id', 'Unknown')}")
        print(f"Visibility: {project_info.get('visibility', 'Unknown')}")
    else:
        print(f"❌ Project access failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Project request failed: {str(e)}")