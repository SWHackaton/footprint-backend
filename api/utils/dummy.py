import requests
from api.utils.crawl import crawl_init,crawl_store,crawl_store_img
from api.utils.coordinate import coor_to_addr,addr_to_coor
from datetime import date,datetime
from random import randint

f = open("dummy.txt", 'w',encoding='utf-8')

# 5ㄱㅐ
address = ['서울 중구 을지로5길 26','서울 중구 삼일대로 358','서울 중구 을지로 99-1', '서울 중구 을지로 88', '서울 영등포구 당산로35길 1','서울 영등포구 영등포로35길 21']

# 6ㄱㅐ
address2 = ['서울 영등포구 당산로 110','서울 영등포구 양산로19길 7','서울 영등포구 당산로27길 12', '서울 영등포구 당산로 128-1','서울 영등포구 국회대로 552','서울 영등포구 영등포로 115','서울 영등포구 영신로44길 23']
user = ['user01','user02']


driver = crawl_init()


def dummy(user,address):
    
    coor_list = []
    addr = address[-1]

    for addr in address:
        tmp  = addr_to_coor(addr)
        tmp2 = coor_to_addr(tmp['x'],tmp['y'])
        coor_list.append({"coor_x" : tmp['x'],"coor_y" :tmp['y'],"addr" : addr,'map_id' : tmp2['map_id'],'dong':tmp2['dong']})
    
    coor = coor_list[0]
    # coor = coor_list[0]

    
    store_list = []

    for coor in coor_list:
        stores = crawl_store(driver,coor["addr"])
        stores = crawl_store_img(stores,coor["dong"])
        for store in stores:
            store['map_id'] = coor['map_id']
            store['dong'] = coor['dong']
            store['longtitude'] = coor['coor_x']
            store['latitude'] = coor['coor_y']
        store_list.append(stores)

    
    # Address_tbl
    for coor in coor_list:
        f.write(f"insert into address_tbl(map_id,addr,longtitude,latitude) values ('{coor['map_id']}','{coor['addr']}','{coor['coor_x']}','{coor['coor_y']}');\n")

    # store_table
    for stores_per_addr in store_list:
        for store in stores_per_addr:
            f.write(f"insert into store_tbl(map_id,store_name,category,img,dong,longtitude,latitude) values('{store['map_id']}','{store['store_name']}','{store['store_category']}','{store['img']}','{store['dong']}',{store['longtitude']},{store['latitude']});\n")
    
    
    # visit_table
    year,month = 2022,6
    hour = 30
    day = hour // 24
    for visit in coor_list:
        day = hour // 24
        tmp_hour = hour % 24
        hour += randint(1,4)
        start_datetime = datetime(year,month,day,tmp_hour).strftime('%Y-%m-%d %H:%M:%S')
        end_datetime = datetime(year,month,day,tmp_hour,30).strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"insert into visit_tbl(user_id,map_id,addr,start_datetime,end_datetime) values ('{user}','{visit['map_id']}','{visit['addr']}','{start_datetime}','{end_datetime}');\n" )
        

dummy('user01',address)
dummy('user02',address2)

f.close()