from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth_ro, gps_ro, diary_ro

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

@app.get("/")
async def root():
	return { "message" : "Hello World" }