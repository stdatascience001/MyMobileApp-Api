from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.trips import router as trips_router

import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Migrations handled by alembic now
    yield

app = FastAPI(title="Travel Companion API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(trips_router, prefix="/api/trips", tags=["trips"])

@app.get("/")
def read_root():
    return {"message": "Travel Companion API is running!"}