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
    'meal': [],
    'drink': [],
    'shopping': [],
    'culture': [],
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
