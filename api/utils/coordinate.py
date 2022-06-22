import json
import requests

# 한글 주소 -> 좌표 변환 함수
def addr_to_coor(addr):
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"

    headers = {
        "X-NCP-APIGW-API-KEY-ID" : "wyp36l1bx2",
        "X-NCP-APIGW-API-KEY" : "9Vlu7QV7pW9rfVueQKeCleGzndVo5mVQXv261iiu"
    }

    params = {
        "coords" : "", # 입력 좌표 ex) coords=128.12345,37.98776
        "output" : "json",
        "orders" : "legalcode,admcode,addr,roadaddr"
    }

    params["query"] = addr

    response = requests.get(url, params=params, headers=headers)
    jsonObject = json.loads(response.text)
    return {'x' : jsonObject['addresses'][0]['x'],'y' : jsonObject['addresses'][0]['y']}

def parse_object(object):
    addr = []
    addr.append(object['region']['area1']['name'])
    addr.append(object['region']['area2']['name'])
    addr.append(object['land']['name'])
    addr.append(object['land']['number1'])
    # addr.append(object['land']['number2'])
    
    result = ' '.join(addr)
    if(object['land']['number2'] != ''):
        result = result + '-' + object['land']['number2']
    
    return result

# 좌표 -> 한글 주소 변환 함수
def coor_to_addr(longtitude, latitude):  
    url= "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"

    headers = {
        "X-NCP-APIGW-API-KEY-ID" : "0tjk5al1o8",
        "X-NCP-APIGW-API-KEY" : "O1Zu7PpgF9VOHT3WLy6acbND2cZHKzxQM8J3pg8O"
    }

    params = {
        "coords" : "", # 입력 좌표 ex) coords=128.12345,37.98776
        "output" : "json",
        "orders" : "roadaddr"
    }
    params["coords"] = longtitude + ',' +latitude
    response = requests.get(url, params=params, headers=headers)
    
    jsonObject = json.loads(response.text)

    if(jsonObject['status']['code'] != 0):
        print(jsonObject['status'])
        raise ValueError("Invalid coordinates")

    return parse_object(jsonObject['results'][-1])



