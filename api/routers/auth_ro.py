from typing import Optional
from fastapi import APIRouter, Depends
from fastapi import FastAPI, Depends, Request, Response, Cookie
from fastapi.responses import RedirectResponse, StreamingResponse, FileResponse
import requests
import json
import os

router = APIRouter(
    prefix="/kakao",
    tags=["Kakao"],
    responses={404: {"description": "Not found"}},
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(BASE_DIR, '../secrets.json')
secrets = json.loads(open(SECRET_FILE).read())

@router.get('')
def kakao():
    REST_API_KEY = secrets['REST_API_KEY']
    REDIRECT_URI = "http://127.0.0.1:8000"
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&response_type=code&redirect_uri={REDIRECT_URI}"
    response = RedirectResponse(url)
    return response


@router.get('/auth')
async def kakaoAuth(response: Response, code: Optional[str]="NONE"):
    REST_API_KEY = secrets['REST_API_KEY']
    REDIRECT_URI = 'http://127.0.0.1:8000'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&code={code}&redirect_uri={REDIRECT_URI}'
    _res = requests.post(_url)
    _result = _res.json()
    response.set_cookie(key="kakao", value=str(_result["access_token"]))
    return {"code":_result}


@router.get('/logout')
def kakaoLogout(request: Request, response: Response):
    url = "https://kapi.kakao.com/v1/user/unlink"
    KEY = request.cookies['kakao']
    headers = dict(Authorization=f"Bearer {KEY}")
    _res = requests.post(url,headers=headers)
    response.set_cookie(key="kakao", value=None)
    return {"logout": _res.json()}