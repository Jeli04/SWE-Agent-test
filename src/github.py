import os
import requests

# GitHub API URL
GITHUB_API_URL = "https://api.github.com"

# Retrieve your GitHub token from the environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("Please set your GITHUB_TOKEN environment variable.")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_github_issue(owner: str, repo: str, issue_number: int) -> dict:
    """
    Retrieves a GitHub issue's details.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_github_pr(owner: str, repo: str, pr_number: int) -> dict:
    """
    Retrieves a GitHub pull request's details.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def create_pull_request(owner, repo, issue_number, branch_name, base="main"):
    headers = {}
    
    # Retrieve the issue details from GitHub
    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    issue_response = requests.get(issue_url, headers=headers)
    if issue_response.status_code != 200:
        print("Error retrieving issue details:", issue_response.content)
        return None
    issue_details = issue_response.json()
    
    # Check if the issue already has a linked pull request.
    # GitHub's API adds a 'pull_request' key if the issue is or is linked to a PR.
    if "pull_request" in issue_details:
        print(f"Issue #{issue_number} already has a linked pull request. Skipping creation.")
        return None

    # Construct the PR title and body.
    issue_title = issue_details.get("title", "").strip()
    issue_body = issue_details.get("body", "")
    pr_title = f"[#{issue_number}] {issue_title}"
    pr_body = f"Closes #{issue_number}\n\n{issue_body}"
    
    # Prepare the payload to create the pull request.
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    payload = {
        "title": pr_title,
        "body": pr_body,
        "head": branch_name,
        "base": base
    }
    print(payload)
    
    # Create the pull request.
    pr_response = requests.post(pr_url, headers=headers, json=payload)
    if pr_response.status_code != 201:
        print("Error creating pull request:", pr_response.content)
        return None
    pr = pr_response.json()
    print("Created PR:", pr.get("html_url", ""))
    return pr

def total_prs(owner, repo, head, base):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    params = {"head": f"{owner}:{head}", "base": base, "state": "all"}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return len(response.json()) 

def main():
    owner = "Jeli04"
    repo = "SWE-Agent-test"
    issue_number = 4

    # Retrieve the issue details
    issue_details = get_github_issue(owner, repo, issue_number)
    issue_title = issue_details.get("title", "").strip()
    print("Issue Title:", issue_title)
    print("Issue Details:", issue_details['body'])

    # Use the correct branch name format without remotes/origin/
    branch_name = "test"  # Modified this line

    head = branch_name  
    base = "main"

    # Print the number of PRs 
    num_prs = total_prs(owner, repo, head, base)
    print("Number of PRs:", num_prs)

    # Create the pull request
    try:
        pr_response = create_pull_request(owner, repo, issue_number, branch_name, base="main")
    except requests.exceptions.HTTPError as e:
        print(f"Error creating PR: {e.response.json()}")

if __name__ == "__main__":
    main()