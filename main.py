import os

from googleapiclient import discovery

# replace these values with your own values
# refer to https://cloud.google.com/cloud-build/docs/api/reference/rest/Shared.Types/Build
PROJECT_ID = os.environ.get("GCP_PROJECT")
REPO_NAME = "repo"
TAG_NAME = "tag"
DIR = "dir"


def trigger(data, context):
    try:
        # https://cloud.google.com/cloud-build/docs/api/reference/rest/v1/projects.builds/create
        service = discovery.build("cloudbuild", "v1", cache_discovery=False)
        body = {
            "source": {
                "repoSource": {
                    "repoName": REPO_NAME,
                    "tagName": TAG_NAME, 
                    "dir": DIR,
                }
            },
            # define the Cloud Build steps
            "steps": [
                {
                    "name": "gcr.io/cloud-builders/gsutil",
                    "id": "Move file from a GCS bucket to another GCS bucket",
                    "args": [
                        "mv",
                        "gs://bucket-a/file.zip",
                        "gs://bucket-b/file.zip",
                    ],
                }
            ],
            "timeout": "3600s",
        }

        service.projects().builds().create(
            projectId=PROJECT_ID, body=body
        ).execute()
    except Exception as e:
        print(e)
        raise(e)
