from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import json

from app.core.database import get_db, SessionLocal
from app.models.user import User
from app.models.trip import Trip
from app.schemas import TripCreate, TripUpdate, TripResponse
from app.core.security import get_current_user

router = APIRouter()

async def generate_itinerary_background(trip_id: UUID):
    from app.services.ai_service import generate_trip_plan
    from app.schemas.ai import TripPlanRequest

    trip = None

    async with SessionLocal() as db:
        try:
            result = await db.execute(select(Trip).where(Trip.uuid == trip_id))
            trip = result.scalars().first()
            if not trip:
                return

            request = TripPlanRequest(
                destination=trip.destination,
                start_date=trip.start_date.isoformat() if hasattr(trip.start_date, 'isoformat') else str(trip.start_date),
                end_date=trip.end_date.isoformat() if hasattr(trip.end_date, 'isoformat') else str(trip.end_date),
                preferences=[str(trip.preferences)] if trip.preferences else []
            )

            # Note: generate_trip_plan is blocking, ideally it should run in an executor
            # or use async version of genai if available, but background_tasks handles it in a threadpool in FastAPI.
            plan = generate_trip_plan(request)
            trip.itinerary_json = plan.model_dump()
            trip.is_generated = True
            await db.commit()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Failed to generate itinerary: {e}")
            if trip is not None:
                trip.itinerary_json = {"error": f"Failed to generate itinerary. Please try again. ({e})"}
                trip.is_generated = True
                await db.commit()

@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    trip: TripCreate, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_trip = Trip(
        user_uuid=current_user.uuid,
        title=trip.title,
        destination=trip.destination,
        start_date=trip.start_date,
        end_date=trip.end_date,
        preferences=trip.preferences,
        is_generated=False,
        itinerary_json=None
    )
    db.add(db_trip)
    await db.commit()
    await db.refresh(db_trip)
    
    background_tasks.add_task(generate_itinerary_background, db_trip.uuid)
    
    return db_trip

@router.get("/", response_model=list[TripResponse])
async def get_trips(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Trip).where(Trip.user_uuid == current_user.uuid))
    trips = result.scalars().all()
    for trip in trips:
        if trip.is_generated is None:
            trip.is_generated = False
    return trips

@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(
    trip_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Trip).where(Trip.uuid == trip_id, Trip.user_uuid == current_user.uuid)
    )
    trip = result.scalars().first()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    if trip.is_generated is None:
        trip.is_generated = False
        
    return trip

@router.post("/{trip_id}/retry", response_model=TripResponse)
async def retry_generation(
    trip_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Trip).where(Trip.uuid == trip_id, Trip.user_uuid == current_user.uuid)
    )
    trip = result.scalars().first()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    trip.is_generated = False
    trip.itinerary_json = None
    await db.commit()
    await db.refresh(trip)
    
    background_tasks.add_task(generate_itinerary_background, trip.uuid)
    return trip

@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: UUID,
    trip_update: TripUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Trip).where(Trip.uuid == trip_id, Trip.user_uuid == current_user.uuid)
    )
    db_trip = result.scalars().first()
    
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    update_data = trip_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_trip, key, value)
        
    await db.commit()
    await db.refresh(db_trip)
    return db_trip

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(
    trip_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Trip)
        .options(selectinload(Trip.itineraries), selectinload(Trip.places))
        .where(Trip.uuid == trip_id, Trip.user_uuid == current_user.uuid)
    )
    db_trip = result.scalars().first()
    
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    await db.delete(db_trip)
    await db.commit()
    return None
