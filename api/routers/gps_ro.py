from fastapi import APIRouter
from typing import Optional
from datetime import date

router = APIRouter(
    prefix = "/gps",
    tags = ["Gps"],
    responses = {404: {"description": "Not Found"}},
)

@router.get("/map")
def getAdress(longitute: float, latitude: float, user_id: str, map_id: Optional[str]=None):
    if not map_id:
        pass
        #위도, 경도 이용해서 위치 정보 값 찾고 db 저장(지도 api)해서 mapid 넘기기
    if map_id:
        return {"map_id": map_id}

@router.get("/timeline")
def getVisit(date: date, user_id: str):
    # 그날 방문한 장소를 모두 불러와 리스트 리턴.
    pass

@router.get("/timeline/store")
def getOneStore(visit_id: int, store_name: str):
    # 한 가게를 선택하면 visit db에 저장
    pass
    