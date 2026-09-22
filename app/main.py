from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.auth import router as auth_router

app = FastAPI(title="Travel Companion API")

@app.on_event("startup")
async def startup():
    pass # Migrations handled by alembic now

app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Travel Companion API is running!"}