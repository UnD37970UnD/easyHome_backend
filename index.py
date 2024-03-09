from fastapi import FastAPI

from routes.listnings import listnings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listnings)

@app.get("/")
def read_root():
    return {"route": "Home"}