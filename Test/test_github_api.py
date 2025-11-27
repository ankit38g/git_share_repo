import requests

# Load your GitHub token
GITHUB_USERNAME = "ankit38g"
GITHUB_TOKEN = ""    # token

# Repo you want to test
REPO = "ankit38g/product-affinity-training"
ENDPOINT = "commits"   # or "issues", "pulls", etc.

url = f"https://api.github.com/repos/{REPO}/{ENDPOINT}"

print("Requesting:", url)

response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))

print("Status Code:", response.status_code)

if response.status_code != 200:
    print("Error Response:", response.text)
else:
    print("Success! Showing first item:")
    print(response.json()[0])