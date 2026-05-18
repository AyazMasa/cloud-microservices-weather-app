import os

import requests
from flask import Flask, render_template, request


app = Flask(__name__)

GEOCODING_SERVICE_URL = os.getenv(
    "GEOCODING_SERVICE_URL", "http://geocoding-service:5001"
)
WEATHER_SERVICE_URL = os.getenv("WEATHER_SERVICE_URL", "http://weather-service:5002")


@app.get("/")
def index():
    return render_template("index.html", city="")


@app.post("/search")
def search():
    city = request.form.get("city", "").strip()
    if not city:
        return render_template(
            "index.html", city=city, error="Please enter a city name."
        ), 400

    try:
        geo_response = requests.get(
            f"{GEOCODING_SERVICE_URL}/geocode",
            params={"city": city},
            timeout=5,
        )
        geo_response.raise_for_status()
        location = geo_response.json()
    except requests.Timeout:
        return render_service_error(city)
    except (requests.RequestException, ValueError):
        return render_service_error(city)

    if not location.get("found"):
        return render_template(
            "index.html", city=city, error="City was not found. Please try another name."
        )

    try:
        weather_response = requests.get(
            f"{WEATHER_SERVICE_URL}/forecast",
            params={"lat": location["latitude"], "lon": location["longitude"]},
            timeout=5,
        )
        weather_response.raise_for_status()
        weather = weather_response.json()
    except (KeyError, requests.Timeout):
        return render_service_error(city)
    except (requests.RequestException, ValueError):
        return render_service_error(city)

    return render_template(
        "index.html", city=city, location=location, weather=weather
    )


def render_service_error(city):
    return render_template(
        "index.html",
        city=city,
        error="Weather lookup is temporarily unavailable. Please try again later.",
    ), 502


@app.get("/health")
def health():
    return {"status": "ok", "service": "webapp"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
