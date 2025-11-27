import os
import requests
import nilus

@nilus.source
def github_source(repo: str, endpoint: str):
    """
    Nilus Custom Source to fetch GitHub API data using:
    - Repo: owner/repo
    - Endpoint: commits, issues, pulls, etc.

    Example:
        custom://github_source?repo=ankit38g/product-affinity-training&endpoint=commits
    """

    username = os.getenv("GITSYNC_USERNAME")
    token = os.getenv("GITSYNC_PASSWORD")

    if not token:
        raise Exception("GitHub token missing. Expected in env: GITSYNC_PASSWORD")

    api_url = f"https://api.github.com/repos/{repo}/{endpoint}"

    headers = {
        "Authorization": f"token {token}",
        "User-Agent": username or "nilus-github-source"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error: {response.status_code} → {response.text}"
        )

    data = response.json()

    # Ensure proper iteration: response should be a list
    if isinstance(data, dict):
        # Sometimes GitHub returns a dict (e.g., rate limit)
        yield data
        return

    for item in data:
        yield item