import os
import requests
import nilus
import dlt
from nilus import CustomSource


# ---------------------------------------------------------
# 1) Nilus expects at least one CustomSource subclass
# ---------------------------------------------------------
class GitHubApiSource(CustomSource):
    def handles_incrementality(self) -> bool:
        return False

    # Not used, but must exist
    def nilus_source(self, uri: str, table: str, **kwargs):
        pass


# ---------------------------------------------------------
# 2) Actual GitHub Source Logic (function-based)
# ---------------------------------------------------------
class GitHubApiRunner:

    def __call__(self, repo: str, endpoint: str):
        print(f"[GitHubApiRunner] repo={repo}")
        print(f"[GitHubApiRunner] endpoint={endpoint}")

        username = os.getenv("GITSYNC_USERNAME")
        token = os.getenv("GITSYNC_PASSWORD")

        if not token:
            raise Exception("GitHub token missing. Expected: GITSYNC_PASSWORD")

        url = f"https://api.github.com/repos/{repo}/{endpoint}"

        headers = {
            "Authorization": f"token {token}",
            "User-Agent": username or "nilus-github-source"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code} → {response.text}")

        data = response.json()

        if isinstance(data, dict):
            data = [data]

        @dlt.resource(name="github_commits")
        def github_commits():
            for item in data:
                yield item

        return github_commits


# ---------------------------------------------------------
# 3) Nilus wrapper — the entrypoint specified in yaml
# ---------------------------------------------------------
@nilus.source
def GitHubApiSource_wrapper(repo: str, endpoint: str):
    runner = GitHubApiRunner()
    return runner(repo, endpoint)