from fastapi import APIRouter
from pydantic import BaseModel
import requests
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

class GoodFirstIssueRequest(BaseModel):
    language: Optional[list[str]] = None
    label: Optional[str] = None
    limit: Optional[int] = None
    username: Optional[str] = None

GITHUB_API_URL = "https://api.github.com"

class GoodFirstIssueResult(BaseModel):
    repository: str
    repo_open_issues: int
    issue_title: str
    issue_url: str
    issue_count: int
    language: str
    issue_created_at: str
    issue_labels: list[str]

@router.post("/")
def good_first_issue(request: GoodFirstIssueRequest):
    try:
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

        label = request.label or "good first issue"
        language = request.language
        limit = request.limit or 10
        username = request.username or GITHUB_USERNAME

        if not GITHUB_USERNAME or not GITHUB_TOKEN:
            return {
                "status_code": 400,
                "message": "GITHUB_USERNAME and GITHUB_TOKEN are required",
                "results": []
            }
        headers = {"Accept": "application/vnd.github+json"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

        if language == None:
            query = (
                f"q=user:{username}+"
                f"label:\"{label}\"+state:open+is:issue"
                f"&sort=created&order=desc&per_page={limit}"
            )
        else:
            language_filter = "+".join([f"language:{lang}" for lang in language])
            query = (
                f"q=user:{username}+{language_filter}+"
                f"label:\"{label}\"+state:open+is:issue"
                f"&sort=created&order=desc&per_page={limit}"
            )

        url = f"{GITHUB_API_URL}/search/issues?{query}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {
                "status_code": response.status_code,
                "message": f"Error: {response.status_code}",
                "results": []
            }
        items = response.json().get("items", [])
        results = []

        for item in items:
            repo_url = item["repository_url"]
            repo_resp = requests.get(repo_url, headers=headers)
            repo_data = repo_resp.json()

            results.append(
                GoodFirstIssueResult(
                    repository = repo_url.replace(f"{GITHUB_API_URL}/repos/{username}/", ""),
                    repo_open_issues = repo_data.get("open_issues"),
                    issue_title = item.get("title"),
                    issue_url = item.get("html_url"),
                    issue_count = len(item.get("labels", [])),
                    language= repo_data.get("language"),
                    issue_created_at = item.get("created_at"),
                    issue_labels = [f"{label["name"]} - {label["description"]}" for label in item.get("labels", [])]
                )
            )
        count = len(results)
        if not results:
            return {
                "status_code": 404,
                "count": count,
                "message": "No good first issue found",
                "results": []
            }

        return {
            "status_code": 200,
            "count": count,
            "message": "Good first issue found",
            "results": results
        }
    except Exception as err:
        return {
            "status_code": 500,
            "count": 0,
            "message": f"Error occurred: {str(err)}",
            "results": []
        }