import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


@app.get("/forecast")
def forecast():
    lat = request.args.get("lat", "").strip()
    lon = request.args.get("lon", "").strip()

    if not lat or not lon:
        return jsonify({"error": "lat and lon parameters are required"}), 400

    try:
        latitude = float(lat)
        longitude = float(lon)
    except ValueError:
        return jsonify({"error": "lat and lon must be numeric"}), 400

    try:
        response = requests.get(
            OPEN_METEO_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min",
                "forecast_days": 3,
                "timezone": "auto",
            },
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
    except requests.Timeout:
        return jsonify({"error": "weather request timed out"}), 504
    except requests.RequestException:
        return jsonify({"error": "weather service request failed"}), 502
    except ValueError:
        return jsonify({"error": "invalid weather service response"}), 502

    try:
        current = data["current"]
        daily = data["daily"]
        forecast_days = [
            {
                "date": date,
                "temp_max": temp_max,
                "temp_min": temp_min,
            }
            for date, temp_max, temp_min in zip(
                daily["time"],
                daily["temperature_2m_max"],
                daily["temperature_2m_min"],
            )
        ]
        return jsonify(
            {
                "current": {
                    "temperature": current["temperature_2m"],
                    "wind_speed": current["wind_speed_10m"],
                },
                "forecast": forecast_days,
            }
        )
    except (KeyError, TypeError):
        return jsonify({"error": "invalid weather service response"}), 502


@app.get("/health")
def health():
    return {"status": "ok", "service": "weather-service"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
