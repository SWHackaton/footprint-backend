import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth_ro, gps_ro, diary_ro, store_ro
from api import models, database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(auth_ro.router)
app.include_router(gps_ro.router)
app.include_router(diary_ro.router)
app.include_router(store_ro.router)


models.Base.metadata.create_all(database.engine)

@app.get("/")
async def root():
	return { "message" : "Hello World" }


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
