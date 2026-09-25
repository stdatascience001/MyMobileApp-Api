import json
from google import genai
from google.genai import types
from app.core.config import settings
from app.schemas.ai import TripPlanRequest, TripPlanResponse

# Initialize the client. We assume GEMINI_API_KEY is available in the environment/settings.
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_trip_plan(request: TripPlanRequest) -> TripPlanResponse:
    prompt = f"""
    Create a detailed trip itinerary for {request.destination} 
    from {request.start_date} to {request.end_date}.
    User preferences for the trip are: {', '.join(request.preferences)}.
    Provide the response strictly as a JSON object matching the requested schema.
    """
    
    response = client.models.generate_content(
        model='"gemini-3.8-flash"',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TripPlanResponse,
            temperature=0.7,
        ),
    )
    
    # Parse the structured JSON response and validate through Pydantic
    try:
        text = response.text
        if text is None:
            raise ValueError("AI response was empty.")
        data = json.loads(text)
        return TripPlanResponse(**data)
    except Exception as e:
        raise ValueError(f"Failed to parse and validate AI response: {e}")

def chat_with_ai(message: str) -> str:
    response = client.models.generate_content(
        model='"gemini-3.8-flash"',
        contents=message,
    )
    text = response.text
    if text is None:
        raise ValueError("AI response was empty.")
    return text
