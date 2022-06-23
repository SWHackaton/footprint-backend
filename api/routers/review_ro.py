from fastapi import APIRouter, Depends

from api.database import get_db
from sqlalchemy.orm import Session

from api.models import Review

router = APIRouter(
    prefix = "/review",
    tags = ["Review"],
    responses = {404: {"description": "Not Found"}},
)


@router.get("/read")
def readDiary(store_name: str, addr: str,db: Session = Depends(get_db)):
    #visit table 내용 불러와 보여주기
    
    review_list = db.query(Review).filter_by(store_name=store_name,addr=addr).all()

    return review_list
    