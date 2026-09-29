import json
from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.ai import TripPlanRequest, TripPlanResponse


# Initialize Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_trip_plan(request: TripPlanRequest) -> TripPlanResponse:
    from datetime import datetime

    try:
        month = datetime.strptime(
            request.start_date,
            "%Y-%m-%d"
        ).strftime("%B")
    except ValueError:
        month = "the time of travel"

    prompt = f"""
You are an expert travel planner.

Create a detailed and realistic trip itinerary for:
Destination: {request.destination}
Start date: {request.start_date}
End date: {request.end_date}
Travel month: {month}

User preferences:
{', '.join(request.preferences)}

Critical Rules:

1. Realistic pacing:
   Limit activities to a maximum of 3-4 places per day.

2. Proximity:
   Group locations by neighborhood to minimize travel time.

3. Hotels:
   Provide exactly 3 hotel recommendations.

4. Restaurants:
   Provide exactly 3 restaurant recommendations.

5. Activities:
   Make the itinerary practical and suitable for the travel dates.

6. Return ONLY a JSON object matching the requested schema.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TripPlanResponse,
            temperature=0.7,
        ),
    )

    try:
        text = response.text

        if not text:
            raise ValueError("AI response was empty.")

        data = json.loads(text)

        return TripPlanResponse(**data)

    except Exception as e:
        raise ValueError(
            f"Failed to parse and validate AI response: {e}"
        )


def chat_with_ai(message: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=message,
    )

    text = response.text

    if not text:
        raise ValueError("AI response was empty.")

    return text