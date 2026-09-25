from fastapi import APIRouter, HTTPException
from app.schemas.ai import ChatRequest, ChatResponse, TripPlanRequest, TripPlanResponse
from app.services import ai_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def ai_chat(request: ChatRequest):
    try:
        reply = ai_service.chat_with_ai(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/plan-trip", response_model=TripPlanResponse)
def ai_plan_trip(request: TripPlanRequest):
    try:
        itinerary = ai_service.generate_trip_plan(request)
        return itinerary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
