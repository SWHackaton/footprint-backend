from typing import Union

from fastapi import APIRouter, Depends
from api import database, models
from sqlalchemy.orm import Session
from api.schemas import diary_sc
from sqlalchemy import and_

router = APIRouter(
    prefix="/store",
    tags=["Store"],
    responses={404: {"description": "Not Found"}},
)

get_db = database.get_db

categories = {
    'meal': ['인도음식', '중식', '베트남음식', '참치회', '제과,베이커리', '중화요리', '분식', '장어', '오리'],
    'drink': ['카페', '커피전문점'],
    'shopping': ['의류판매', '화장품', '가발', '건강식품판매', '상가,아케이드', '남성의류ㅡ양복'],
    'culture': ['컴퓨터학원', '노래방', '미용실', '음악학원', '음악', '미술학원'],
    'travel': [],
    'hotel': [],
    'subway': [],
    'bus': [],
    'airplane': []
}

@router.get("/search")
def searchStore(q: Union[str, None] = None, db: Session = Depends(get_db)):
    query = db.query(models.Store).filter(models.Store.store_name.ilike(f'%{q}%')).all()
    return {
        'status': 'ok',
        'result': query
    }


@router.get("/category/{category}")
def getCategory(category: str, db: Session = Depends(get_db)):
    query = db.query(models.Store).filter(models.Store.category.in_(categories.get(category))).all()
    return {
        'status': 'ok',
        'result': query
    }
