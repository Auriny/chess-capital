from fastapi import FastAPI


app = FastAPI(prefix="/api/v1/cv")

@app.get("/")
async def root():
    return {"message": "Hello World"}