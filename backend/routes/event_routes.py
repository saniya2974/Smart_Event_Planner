from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from config import events_collection
from services.weather_service import get_weather_forecast, calculate_score
from models.event_model import validate_event
from datetime import datetime
from collections import defaultdict

event_routes = Blueprint("event_routes", __name__)

# Create event
@event_routes.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    valid, msg = validate_event(data)
    if not valid:
        return jsonify({"error": msg}), 400

    result = events_collection.insert_one(data)
    return jsonify({"message": "Event created", "id": str(result.inserted_id)})

# List all events
@event_routes.route("/events", methods=["GET"])
def list_events():
    events = list(events_collection.find())
    for event in events:
        event["_id"] = str(event["_id"])
    return jsonify(events)

# Analyze weather and give 5-day forecast with scores
@event_routes.route("/events/<id>/weather-check", methods=["POST"])
def weather_check(id):
    event = events_collection.find_one({"_id": ObjectId(id)})
    if not event:
        return jsonify({"error": "Event not found"}), 404

    city = event.get("location", "")
    event_type = event.get("type", "")
    event_date = str(event.get("date", ""))[:10]  # Ensures format 'YYYY-MM-DD'

    forecast_data = get_weather_forecast(city)
    if "list" not in forecast_data:
        return jsonify({"error": "Forecast data unavailable"}), 500

    from collections import defaultdict
    from datetime import datetime

    daily_forecast = defaultdict(list)
    for entry in forecast_data["list"]:
        date_str = entry["dt_txt"].split(" ")[0]
        daily_forecast[date_str].append(entry)

    summary = []
    for i, (date, entries) in enumerate(daily_forecast.items()):
        if i >= 5:
            break  # Limit to 5 days

        temps = [e.get("main", {}).get("temp", 0) for e in entries]
        winds = [e.get("wind", {}).get("speed", 0) for e in entries]
        precs = [e.get("rain", {}).get("3h", 0) for e in entries]

        temp = sum(temps) / len(temps)
        wind = sum(winds) / len(winds)
        precip = sum(precs) / len(precs)

        score = calculate_score(temp, precip, wind, event_type)
        label = "Good" if score >= 80 else "Okay" if score >= 60 else "Poor"

        summary.append({
            "date": date,
            "temp": round(temp, 1),
            "wind": round(wind, 1),
            "precip": round(precip, 1),
            "score": score,
            "suitability": label
        })

    # Suggestion logic
    suggestion = {}
    original_day = None
    for d in summary:
        if d["date"] == event_date:
            original_day = d
            break

    if original_day and original_day["score"] < 60:
        # Try to find a better day
        better_day = next((d for d in summary if d["date"] != event_date and d["score"] >= 60), None)
        if better_day:
            suggestion["message"] = f"Try {better_day['date']} instead ({better_day['suitability']})"
        else:
            suggestion["message"] = "No better day found this week."

    # Save to DB
    events_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "weather": summary,
            "suggestion": suggestion
        }}
    )

    return jsonify({"forecast": summary, "suggestion": suggestion})
