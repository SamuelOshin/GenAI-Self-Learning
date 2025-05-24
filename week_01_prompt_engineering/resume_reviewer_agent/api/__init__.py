from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Resume Reviewer API")

@app.get("/")
async def root():
    return {"message": "Welcome to Resume Reviewer Agent!"}

app.include_router(router, prefix="/api", tags=["resume-review"])
