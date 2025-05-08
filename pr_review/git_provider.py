import os
import boto3
import json
import time
import requests
from github import Github
from github import Auth
from dotenv import load_dotenv
from datetime import datetime, timezone
from dateutil import tz
from zoneinfo import ZoneInfo


# Received PR Request: 
# {
#     "pr_number": "16",
#     "repo": "ississippi/pull-request-test-repo",
#     "pr_title": "Update the POST url for the new lambda",
#     "user_login": "ississippi",
#     "created_at": "2025-04-26T19:13:22Z",
#     "pr_state": "open",
#     "pr_body": "",
#     "html_url": "https://github.com/ississippi/pull-request-test-repo/pull/16",
#     "head_sha": "45a7b179af22cb9ceb62084c22bc03d81543cf79",
#     "base_ref": "main"
# }
# owner = "ccxt"
# repo = "ccxt"
# owner = "ississippi"
# repo = "JupyterLearning"
owner = "TheAlgorithms"
repo = "Python"
owner = "public-apis"
repo = "public-apis"
pull_number = 25653  # Replace with the desired PR number
url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}"
pulls_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
# vinta_pulls = "https://api.github.com/vinta/awesome-python/pulls"  # Example for a different repo

load_dotenv()
# Create an SSM client
ssm = boto3.client('ssm')
def get_parameter(name):
    """Fetch parameter value from Parameter Store"""
    response = ssm.get_parameter(
        Name=name,
        WithDecryption=True
    )
    return response['Parameter']['Value']
# Load secrets at cold start

if __name__ == "__main__":
    # Load environment variables from .env file
    GIT_API_KEY = os.getenv("GIT_API_KEY")
    if GIT_API_KEY is None:
        raise ValueError("GIT_API_KEY not found in environment variables.")
else:
    # Load environment variables from .env file
    GIT_API_KEY = get_parameter("/prreview/GIT_API_KEY")
    if GIT_API_KEY is None:
        raise ValueError("GIT_API_KEY not found in parameter store.")

headers = {
    "Accept": "application/vnd.github.v3+json",
    # Optional: Add token for higher rate limits
    # "Authorization": "Bearer YOUR_TOKEN"
}

def get_pr_details():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pr_data = response.json()
        print("PR Title:", pr_data["title"])
        print("Source Branch:", pr_data["head"]["ref"])
        print("Target Branch:", pr_data["base"]["ref"])
        print("Diff URL:", pr_data["diff_url"])
    else:
        print(f"Error: {response.status_code}, {response.json().get('message')}")

def get_pr_diff(repo,pr_number):
    # Headers for diff request
    diff_headers = {
        "Accept": "application/vnd.github.v3.diff",
    }
    token = GIT_API_KEY
    # print(f"Using GitHub API Key: {token}")
    if token:
        headers["Authorization"] = f"token {token}"

    # Construct the diff URL
    url = f"https://github.com/{repo}/pull/{pr_number}.diff"
    # Get the diff for this PR
    print(f"Fetching diff for PR #{pr_number} in {repo}...")
    response = requests.get(url, headers=diff_headers)
    if response.status_code == 200:
        diff = response.text
        #print(f'Diff: {diff}')
        return diff
    else:
        print(f"Error: {response.status_code}")

def get_pr_files(owner, repo, pr_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    load_dotenv()  # Load from .env in current directory
    token = GIT_API_KEY
    # print(f"Using GitHub API Key: {token}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "python-script"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses

    files = response.json()
    for file in files:
        filename = file.get("filename")
        status = file.get("status")  # e.g. 'added', 'modified', 'removed'
        print(f"{status.upper()}: {filename}")


def get_pull_requests(state='open'):
    """
    Fetch pull requests from a GitHub repository.
    
    Args:
        owner (str): Repository owner (e.g., 'octocat')
        repo (str): Repository name (e.g., 'hello-world')
        token (str, optional): GitHub Personal Access Token for authentication
        state (str): State of PRs to fetch ('open', 'closed', or 'all')
    
    Returns:
        list: List of pull requests
    """
    load_dotenv()  # Load from .env in current directory
    token = os.environ.get("GIT_API_KEY")
    if token:
        headers["Authorization"] = f"token {token}"
    params = {
        "state": state,
        "per_page": 5  # Maximum number of PRs per page
    }
    
    pull_requests = []
    page = 1
    print(f"Fetching {state} pull requests from {pulls_url}...")
    #while True:
    params["page"] = page
    response = requests.get(pulls_url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        return
    
    prs = response.json()
    # if not prs:  # No more PRs to fetch
    #     break
        
    pull_requests.extend(prs)
    #page += 1
    
    return pull_requests

def print_pull_requests(prs):
    """
    Print basic information about pull requests.
    
    Args:
        prs (list): List of pull requests
    """
    for pr in prs:
        print(f"State: {pr['state'].capitalize()}")
        print(f"{pr['title']}")
        user_name = pr['user']['login'] if 'user' in pr else 'Unknown User'
        created_at = pr['created_at']
        if created_at:
            local_timezone = tz.tzlocal()
            date_object = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            local_time = date_object.astimezone(local_timezone) 
                    
            created_at = local_time.strftime("%Y-%m-%d at %H:%M:%S")
        else:
            created_at = "Unknown Date"
        print(f"PR #{pr['number']} opened by {user_name} on {created_at}")

        print(f"URL: {pr['html_url']}")
        print("-" * 50)

# def git_pr_list():
#     load_dotenv()  # Load from .env in current directory   
#     token = os.environ.get("GIT_API_KEY") 
#     print(f"token: {token}")
#     g = Github("GIT_API_KEY")
#     print(f"g: {g.get_user()}")
    # repo = g.get_repo("public-apis/public-apis")
    # prs = repo.get_pulls(state="open")
    # for pr in prs:
    #     print(f"PR #{pr.number}: {pr.title}")


if __name__ == "__main__":
    load_dotenv()
    owner = "ississippi"
    repo = "pull-request-test-repo"
    pr_number = 16
    # get_pr_details()
    # get_pr_files()
    # get_pr_diff("ississippi/pull-request-test-repo", 16)
    # Fetch pull requests
    # prs = get_pull_requests()
    # # Print results
    # print(f"Found {len(prs)} pull requests:")
    # print_pull_requests(prs)  
    # git_pr_list()  : needs work
    get_pr_files(owner=owner,repo=repo,pr_number=pr_number)
