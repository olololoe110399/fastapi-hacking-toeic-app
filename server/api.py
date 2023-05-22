from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as ToeicRouter

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }

app.include_router(ToeicRouter, prefix="/toeic")