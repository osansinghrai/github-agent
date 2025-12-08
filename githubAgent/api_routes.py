from fastapi import APIRouter
from .good_first_issue import router as GOOD_FIRST_ISSUE
from .get_repo_activity import router as GET_REPO_ACTIVITY
from .summarize_issue import router as SUMMARIZE_ISSUE

router = APIRouter()

# SEARCH GOOD FIRST ISSUE
router.include_router(GOOD_FIRST_ISSUE, prefix="/good-first-issue")

# GET REPO ACTIVITY
router.include_router(GET_REPO_ACTIVITY, prefix="/get-repo-activity")

# SUMMARIZE ISSUE
router.include_router(SUMMARIZE_ISSUE, prefix="/summarize-issue")