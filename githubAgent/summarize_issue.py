from pydantic import BaseModel
from fastapi import APIRouter
import requests
import re
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
class SummarizeIssueRequest(BaseModel):
    issue_url: str

class SummarizeIssueResult(BaseModel):
    issue_count: int
    issue_title: str
    issue_body: str
    issue_label_count: int
    issue_label_names: list[str]
    issue_comments: int
    issue_commits: int

GITHUB_API_URL = "https://api.github.com"

@router.post("/")
def summarize_issue(request: SummarizeIssueRequest):
    try:
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        ISSUE_URL = request.issue_url
        ISSUE_NUMBER_FROM_URL = re.search(r"/issues/(\d+)", ISSUE_URL).group(1)
        ISSUE_NUMBER = ISSUE_NUMBER_FROM_URL

        GITHUB_USERNAME = re.search(r"https://github\.com/([^/]+)/([^/]+)", ISSUE_URL).group(1)
        GITHUB_REPO_NAME = re.search(r"https://github\.com/([^/]+)/([^/]+)", ISSUE_URL).group(2)

        headers = {"Accept": "application/vnd.github+json"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

        url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}/issues/{ISSUE_NUMBER}"
        response = requests.get(url, headers=headers)
        issue_data = response.json()

        results = []

        results.append(
            SummarizeIssueResult(
                issue_count = issue_data.get("number"),
                issue_title = issue_data.get("title"),
                issue_body = issue_data.get("body"),
                issue_label_count = len(issue_data.get("labels", [])),
                issue_label_names = [label.get("name") for label in issue_data.get("labels", [])],
                issue_comments = issue_data.get("comments", 0),
                issue_commits = issue_data.get("commits", 0)
            )
        )

        count = len(results)

        if not results:
            return {
                "status_code": 404,
                "message": "No issue found",
                "count": count,
                "results": []
            }

        return {
            "status_code": 200,
            "count": count,
            "message": "Issue found",
            "results": results
        }

    except Exception as err:
        return {
            "status_code": 500,
            "count": 0,
            "message": f"Error occurred: {str(err)}",
            "results": []
        }