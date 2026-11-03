from fastapi import FastAPI
from myproject.router import router

app = FastAPI()

app.include_router(router)
