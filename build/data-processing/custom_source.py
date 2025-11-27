import os
import requests
import nilus
from nilus import CustomSource

@nilus.source
def github_source(repo: str, endpoint: str):

    username = os.getenv("GITSYNC_USERNAME")
    token = os.getenv("GITSYNC_PASSWORD")

    if not token:
        raise Exception("GitHub token missing (GITSYNC_PASSWORD)")

    api_url = f"https://api.github.com/repos/{repo}/{endpoint}"

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": username or "nilus-github-source"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error: {response.status_code} → {response.text}"
        )

    data = response.json()
    if isinstance(data, dict):
        yield data
        return

    for item in data:
        yield item


# ----------------------------------------------------
# 🔥 REQUIRED WRAPPER: Nilus wants a CustomSource class
# ----------------------------------------------------
class GitHubApiSource(CustomSource):
    """
    Wrapper class required by Nilus.
    It simply maps the URI parameters to github_source().
    """

    def nilus_source(self, repo: str, endpoint: str, **kwargs):
        return github_source(repo=repo, endpoint=endpoint)