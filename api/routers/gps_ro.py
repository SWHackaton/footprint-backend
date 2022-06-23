from fastapi import APIRouter, Depends
from typing import Optional
from datetime import date,datetime

from api.database import get_db
from sqlalchemy.orm import Session
from api.utils.coordinate import coor_to_addr

from api.utils.crawl import crawl_init,crawl_store
from api.utils.coordinate import coor_to_addr

from api.models import Address
from api.models import Store
from api.models import Visit


driver = crawl_init()

router = APIRouter(
    prefix = "/gps",
    tags = ["Gps"],
    responses = {404: {"description": "Not Found"}},
)


@router.get("/map")
async def getAdress(longtitude: float, latitude: float, user_id: str, map_id: Optional[str]=None,db: Session = Depends(get_db)):
    if not map_id:
        # Address_tbl 정보 
        result = coor_to_addr(str(longtitude),str(latitude))
        db_address = Address(map_id = result['map_id'], addr = result['address'])

        address_check = db.query(Address).filter_by(map_id = result['map_id']).all()
        if(len(address_check) == 0):
            # store_tbl 정보 -> list
            stores = crawl_store(driver,result['address'])
            db_stores = [Store(map_id = result['map_id'],
                            store_name = store['store_name'],
                            category = store['store_category']) for store in stores ]
            db.add_all(db_stores)
            db.add(db_address)      


        # visit_tbl 정보 
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db_visit = Visit(user_id = user_id,
                        map_id = result['map_id'],
                        addr = result['address'],
                        start_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        end_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


        db.add(db_visit)
        db.commit()


        return {'map_id' : result['map_id']}
        
        #위도, 경도 이용해서 위치 정보 값 찾고 db 저장(지도 api)해서 mapid 넘기기
    if map_id:
        visit_update = db.query(Visit).filter_by(user_id = user_id, map_id = map_id).all()
        visit_update[-1].end_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.add(visit_update[-1])
        db.commit()

        return {"map_id": map_id}

@router.get("/timeline")
def getVisit(date: date, user_id: str,db: Session = Depends(get_db)):
    # 그날 방문한 장소를 모두 불러와 리스트 리턴.
    visit_list = db.query(Visit).filter_by(user_id=user_id).all()
    result = []
    print(date)
    for visit in visit_list:
        if(date == visit.start_datetime.date()):
            result.append(visit)

    return result

@router.get("/timeline/store")
def getOneStore(visit_id: int, store_name: str,db: Session = Depends(get_db)):
    # 한 가게를 선택하면 visit db에 저장
    visit_update = db.query(Visit).filter_by(visit_id = visit_id).first()
    visit_update.store_name = store_name
    db.add(visit_update)
    db.commit()
    return visit_update


