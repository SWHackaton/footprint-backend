from fastapi import APIRouter

router = APIRouter(
    prefix = "/diary",
    tags = ["Diary"],
    responses = {404: {"description": "Not Found"}},
)

# 다이어리 CRUD