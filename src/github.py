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

def create_pull_request(owner: str, repo: str, head: str, base: str, title: str, body: str = "") -> dict:
    """
    Creates a pull request on GitHub.
    
    Parameters:
      - owner: GitHub username or organization name.
      - repo: Repository name.
      - head: The branch where your changes are implemented.
      - base: The branch you want to merge your changes into (e.g., "main").
      - title: The title of the pull request.
      - body: (Optional) The pull request description.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    payload = {
        "title": title,
        "head": head,
        "base": base,
        "body": body
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    owner = "Jeli04"
    repo = "SWE-Agent-test"
    issue_number = 1

    # Retrieve the issue details
    issue_details = get_github_issue(owner, repo, issue_number)
    issue_title = issue_details.get("title", "").strip()
    print("Issue Title:", issue_title)
    print("Issue Details:", issue_details['body'])

    # Use the correct branch name format without remotes/origin/
    branch_name = "feature/test-branch"  # Modified this line

    head = branch_name  
    base = "main"

    # Create the PR title and body
    pr_title = f"Fix for Issue #{issue_number}: {issue_title}"
    pr_body = f"This pull request addresses the issue and includes the necessary fixes.\n\nCloses #{issue_number}"

    try:
        pr_response = create_pull_request(owner, repo, head, base, pr_title, pr_body)
        print("Created PR URL:", pr_response.get("html_url"))
    except requests.exceptions.HTTPError as e:
        print(f"Error creating PR: {e.response.json()}")

if __name__ == "__main__":
    main()