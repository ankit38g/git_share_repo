import os
import requests
import urllib.parse
import nilus
from nilus import CustomSource


# -------------------------------
# 1. The actual extractor function
# -------------------------------
@nilus.source
def github_source(repo: str, endpoint: str):
    """
    Nilus source implementation that fetches data from the GitHub API.

    Parameters:
        repo (str): GitHub repo in format "owner/repo"
        endpoint (str): API endpoint such as "commits", "issues", "pulls"

    Example full address:
        custom://GitHubApiSource?repo=ankit38g/product-affinity-training&endpoint=commits
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

    # GitHub sometimes returns dict for errors or single object
    if isinstance(data, dict):
        yield data
        return

    for item in data:
        yield item


# ------------------------------------------------
# 2. Nilus Custom Source wrapper (mandatory class)
# ------------------------------------------------
class GitHubApiSource(CustomSource):

    def nilus_source(self, uri: str, table: str, **kwargs):
        """
        Parse the URI:
            custom://GitHubApiSource?repo=X&endpoint=Y

        and pass parameters to github_source().
        """

        parsed = urllib.parse.urlparse(uri)
        params = urllib.parse.parse_qs(parsed.query)

        repo = params.get("repo", [None])[0]
        endpoint = params.get("endpoint", [None])[0]

        if not repo:
            raise ValueError("Missing required parameter: repo")
        if not endpoint:
            raise ValueError("Missing required parameter: endpoint")

        # Debug logs (optional)
        print(f"[GitHubApiSource] repo={repo}")
        print(f"[GitHubApiSource] endpoint={endpoint}")

        # Return the actual Nilus source function
        return github_source(repo=repo, endpoint=endpoint)