from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class TripPlanRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    preferences: List[str]

class Recommendation(BaseModel):
    name: str
    type: str = Field(description="e.g., Attraction, Restaurant, Hotel")
    description: str
    estimated_cost: Optional[str] = None
    rating: Optional[str] = None

class DailyPlan(BaseModel):
    day: str = Field(description="Date or Day identifier, e.g., 'Day 1 - 2026-10-10'")
    morning_activity: str
    lunch_suggestion: str
    afternoon_activity: str
    dinner_suggestion: str
    transit_tips: Optional[str] = None

class TripPlanResponse(BaseModel):
    destination: str
    recommendations: List[Recommendation]
    daily_plan: List[DailyPlan]
