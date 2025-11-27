import os
import requests
import nilus
import dlt


class GitHubApiSource:

    def __init__(self):
        pass

    def __call__(self, repo: str, endpoint: str):
        print(f"[GitHubApiSource] repo={repo}")
        print(f"[GitHubApiSource] endpoint={endpoint}")

        username = os.getenv("GITSYNC_USERNAME")
        token = os.getenv("GITSYNC_PASSWORD")

        if not token:
            raise Exception("GitHub token missing. Expected env var: GITSYNC_PASSWORD")

        url = f"https://api.github.com/repos/{repo}/{endpoint}"

        headers = {
            "Authorization": f"token {token}",
            "User-Agent": username or "nilus-github-source"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code} → {response.text}")

        data = response.json()

        # Always convert dict → list for pipeline
        if isinstance(data, dict):
            data = [data]

        # THE IMPORTANT PART
        @dlt.resource(name="github_commits")
        def github_commits():
            for item in data:
                yield item

        return github_commits


@nilus.source
def GitHubApiSource_wrapper(repo: str, endpoint: str):
    """Nilus entrypoint — DO NOT modify this logic"""
    source = GitHubApiSource()
    return source(repo, endpoint)