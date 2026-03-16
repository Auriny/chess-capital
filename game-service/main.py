from fastapi import FastAPI

from routers import api_router

app = FastAPI(title="Chess Capital Backend")

app.include_router(api_router)
