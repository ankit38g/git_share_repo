import requests
import nilus
from nilus import CustomSource

@nilus.source()
class GitHubApiSource(CustomSource):

    def __init__(self, repo, endpoint, **kwargs):
        super().__init__(**kwargs)
        self.repo = repo
        self.endpoint = endpoint

    def run(self):
        import os

        username = os.getenv("GITSYNC_USERNAME")
        token = os.getenv("GITSYNC_PASSWORD")

        if not token:
            raise Exception("GitHub token not found in environment (GITSYNC_PASSWORD).")

        api_url = f"https://api.github.com/repos/{self.repo}/{self.endpoint}"

        headers = {
            "Authorization": f"token {token}",
            "User-Agent": username or "nilus-github-client"
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"GitHub API error: {response.status_code}, {response.text}"
            )

        data = response.json()

        # Yield each record for Nilus
        for item in data:
            yield item