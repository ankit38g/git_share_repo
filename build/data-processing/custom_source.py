import os
import requests
import nilus

@nilus.source
def github_source(repo: str, endpoint: str):
    """
    Nilus Custom Source to fetch GitHub API data using GitHub REST API.
    Supports pagination automatically.
    """

    username = os.getenv("GITSYNC_USERNAME")
    token = os.getenv("GITSYNC_PASSWORD")

    if not token:
        raise Exception("GitHub token missing (env: GITSYNC_PASSWORD)")

    base_url = f"https://api.github.com/repos/{repo}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": username or "nilus-github-source"
    }

    page = 1
    per_page = 100   # GitHub max per page

    while True:
        url = f"{base_url}?per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"GitHub API error: {response.status_code} → {response.text}"
            )

        data = response.json()

        # If no more data → break
        if not data:
            break

        # Yield all items
        for item in data:
            yield item

        page += 1