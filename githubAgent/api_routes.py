from fastapi import APIRouter
from .good_first_issue import router as GOOD_FIRST_ISSUE

router = APIRouter()

router.include_router(GOOD_FIRST_ISSUE, prefix="/good-first-issue")