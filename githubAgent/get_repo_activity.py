from pydantic import BaseModel
from fastapi import APIRouter
import re
import requests
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

class getRepoActivityRequest(BaseModel):
    repo: str

class GetRepoActivityResult(BaseModel):
    stars: int
    forks: int
    open_issues: int
    issues_url: list[str]
    issues_number: list[int]
    open_prs: int
    prs_url: list[str]
    total_commits: int
    commits_url: list[str]

GITHUB_API_URL = "https://api.github.com"   

@router.post("/")
def get_repo_activity(request: getRepoActivityRequest):
    try:
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        GITHUB_REPO = request.repo

        GITHUB_USERNAME = re.search(r"https://github\.com/([^/]+)/([^/]+)", GITHUB_REPO).group(1)
        GITHUB_REPO_NAME = re.search(r"https://github\.com/([^/]+)/([^/]+)", GITHUB_REPO).group(2)
        
        headers = {"Accept": "application/vnd.github+json"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}"
        response = requests.get(url, headers=headers)

        repo_data = response.json()

        PULL_REQUESTS_URL = f"{url}/pulls?state=open"

        PULL_REQUESTS_URL_RESPONSE = requests.get(PULL_REQUESTS_URL, headers=headers)
        PULL_REQUESTS_URL_DATA = PULL_REQUESTS_URL_RESPONSE.json()
        PRS_URLS = [data.get("html_url") for data in PULL_REQUESTS_URL_DATA]

        COMMITS_URL = f"{url}/commits"
        COMMITS_URL_RESPONSE = requests.get(COMMITS_URL, headers=headers)
        COMMITS_DATA = COMMITS_URL_RESPONSE.json()
        COMMITS_URLS = [data.get("html_url") for data in COMMITS_DATA]

        ISSUES_URL = f"{url}/issues"
        ISSUES_URL_RESPONSE = requests.get(ISSUES_URL, headers=headers)
        ISSUES_URL_DATA = ISSUES_URL_RESPONSE.json()
        ISSUES_URLS = [data.get("html_url") for data in ISSUES_URL_DATA]
        ISSUES_URL_FILTERED = [url for url in ISSUES_URLS if "/issues" in url]
        ISSUES_NUMBERS = []
        for url in ISSUES_URL_FILTERED:
            match = re.search(r"/issues/(\d+)", url)
            if match:
                ISSUES_NUMBERS.append(int(match.group(1)))

        results = []

        results.append(
            GetRepoActivityResult(
                stars = repo_data.get("stargazers_count"),
                forks = repo_data.get("forks_count"),
                open_issues = len(ISSUES_URL_FILTERED),
                issues_url = ISSUES_URL_FILTERED,
                issues_number = ISSUES_NUMBERS,
                open_prs = len(PULL_REQUESTS_URL_DATA),
                prs_url = PRS_URLS,
                total_commits = len(COMMITS_URLS),
                commits_url = COMMITS_URLS
            )
        )

        count = len(results)

        if not results:
            return {
                "status_code": 404,
                "count": count,
                "message": "No repo activity found",
                "results": []
            }
        
        return {
            "status_code": 200,
            "count": count,
            "message": "Repo activity found",
            "results": results
        }
        
    except Exception as err:
        return {
            "status_code": 500,
            "count": 0,
            "message": f"Error occurred: {str(err)}",
            "results": []
        }