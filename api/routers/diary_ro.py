from fastapi import APIRouter

router = APIRouter(
    prefix = "/diary",
    tags = ["Diary"],
    responses = {404: {"description": "Not Found"}},
)

@router.post("/post")
def postDiary(visit_id: int, store_name: str):
    # visit table content update
    pass

@router.get("/read")
def readDiary(visit_id: int, user_id: str):
    #visit table 내용 불러와 보여주기
    pass