import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "cloud-second-project-geocoding-service/1.0"}


@app.get("/geocode")
def geocode():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "city parameter is required"}), 400

    try:
        response = requests.get(
            NOMINATIM_URL,
            params={"q": city, "format": "jsonv2", "limit": 1},
            headers=HEADERS,
            timeout=5,
        )
        response.raise_for_status()
        results = response.json()
    except requests.Timeout:
        return jsonify({"error": "geocoding request timed out"}), 504
    except requests.RequestException:
        return jsonify({"error": "geocoding service request failed"}), 502
    except ValueError:
        return jsonify({"error": "invalid geocoding service response"}), 502

    if not isinstance(results, list):
        return jsonify({"error": "invalid geocoding service response"}), 502

    if not results:
        return jsonify({"found": False, "query": city})

    place = results[0]
    if not isinstance(place, dict):
        return jsonify({"error": "invalid geocoding service response"}), 502

    try:
        latitude = float(place["lat"])
        longitude = float(place["lon"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "invalid geocoding service response"}), 502

    return jsonify(
        {
            "found": True,
            "query": city,
            "display_name": place.get("display_name", city),
            "latitude": latitude,
            "longitude": longitude,
        }
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "geocoding-service"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
