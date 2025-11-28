import os
import requests
import nilus
import dlt
from nilus import CustomSource


# ---------------------------------------------------------
# 1) Nilus class — MUST exist and MUST be named in YAML
# ---------------------------------------------------------
class GitHubApiSource(CustomSource):

    def handles_incrementality(self) -> bool:
        return False

    def nilus_source(self, uri: str, table: str, **kwargs):
        """
        Nilus will call this method with the full URI. 
        We parse parameters and call the actual wrapper.
        """
        from urllib.parse import urlparse, parse_qs

        parsed = urlparse(uri)
        params = parse_qs(parsed.query)

        repo = params.get("repo", [None])[0]
        endpoint = params.get("endpoint", [None])[0]

        if not repo:
            raise Exception("Missing repo=? in URI")
        if not endpoint:
            raise Exception("Missing endpoint=? in URI")

        return GitHubApiSource_wrapper(repo=repo, endpoint=endpoint)


# ---------------------------------------------------------
# 2) The real GitHub API logic
# ---------------------------------------------------------
class GitHubApiRunner:

    def __call__(self, repo: str, endpoint: str):
        print(f"[GitHubApiRunner] repo={repo}")
        print(f"[GitHubApiRunner] endpoint={endpoint}")

        token = os.getenv("GITSYNC_PASSWORD")
        username = os.getenv("GITSYNC_USERNAME")

        if not token:
            raise Exception("GitHub token missing in GITSYNC_PASSWORD")

        url = f"https://api.github.com/repos/{repo}/{endpoint}"

        headers = {
            "Authorization": f"token {token}",
            "User-Agent": username or "nilus-github"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"GitHub API error {response.status_code}: {response.text}")

        data = response.json()
        if isinstance(data, dict):
            data = [data]

        @dlt.resource(name="github_commits_masked")
        def github_commits_masked():
            for row in data:
                yield row

        return github_commits_masked


# ---------------------------------------------------------
# 3) Decorated wrapper — Nilus-friendly
# ---------------------------------------------------------
@nilus.source
def GitHubApiSource_wrapper(repo: str, endpoint: str):
    runner = GitHubApiRunner()
    return runner(repo, endpoint)