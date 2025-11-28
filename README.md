# Getting github data via Nilus utilizing Custom source for API using Python
YAML → Nilus → GitHubApiSource class → nilus_source()
           ↓
       GitHubApiSource_wrapper()
           ↓
     GitHubApiRunner().__call__()
           ↓
    requests.get( GitHub API )
           ↓
     dlt.resource → Nilus Sink

# explaination of each components :
GitHubApiSource :
Required by Nilus + URI parsing

nilus_source() :
Converts Nilus inputs → Python arguments

GitHubApiSource_wrapper :
Nilus-compatible DLT wrapper

GitHubApiRunner :
Actual GitHub API logic

dlt.resource :
Required for Nilus ingestion
