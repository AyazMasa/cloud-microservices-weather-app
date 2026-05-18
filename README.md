# Cloud Microservices Weather App

A student cloud computing project that demonstrates a small service-oriented application with Python Flask and Docker Compose. The app lets a user enter a city name, resolves it to coordinates, and shows current weather plus a 3-day forecast.

## Architecture

The project contains three Flask services:

| Service | Purpose | Port |
|---|---|---|
| `webapp` | Browser UI and request orchestration | `8080 -> 5000` |
| `geocoding-service` | Validates city names and returns latitude/longitude | `5001` |
| `weather-service` | Returns current weather and a 3-day forecast | `5002` |

```text
Browser
  |
  v
webapp
  |
  +--> geocoding-service --> Nominatim API
  |
  +--> weather-service ----> Open-Meteo API
```

The webapp is the only service the user interacts with directly. It calls the geocoding service first, then calls the weather service only when the city is found.

## Technologies Used

- Python 3.12
- Flask
- Requests
- Docker
- Docker Compose
- Nominatim API for city geocoding
- Open-Meteo API for weather data

## Implemented Features

- Web form for city lookup
- Separate Flask services for UI, geocoding, and weather
- Docker Compose networking between services
- Service health endpoints
- Input validation for missing or invalid city names
- Error handling for unavailable upstream services
- External API integration without API keys

## How To Run

Requirements:

- Docker
- Docker Compose
- Internet access for the external APIs

Start the services:

```bash
docker compose up --build
```

Open the webapp:

```text
http://localhost:8080
```

Stop the services:

```bash
docker compose down
```

## Health Checks

```bash
curl http://localhost:8080/health
curl http://localhost:5001/health
curl http://localhost:5002/health
```

## API Smoke Checks

```bash
curl "http://localhost:5001/geocode?city=Kyiv"
curl "http://localhost:5002/forecast?lat=50.4501&lon=30.5234"
```

## Manual Test Checklist

- Search for a valid city such as `Kyiv` or `London`; weather data should be displayed.
- Search for random text; the webapp should show a friendly city-not-found message.
- Stop or block `geocoding-service`; the webapp should show a temporary service error.
- Stop or block `weather-service`; the webapp should show a temporary service error.

## Environment Variables

Docker Compose already sets these values for the `webapp` container:

| Variable | Default in Docker Compose |
|---|---|
| `GEOCODING_SERVICE_URL` | `http://geocoding-service:5001` |
| `WEATHER_SERVICE_URL` | `http://weather-service:5002` |

See `.env.example` for non-secret example values.

## Project Structure

```text
docker-compose.yml
.env.example
.gitignore
README.md
webapp/
  app.py
  Dockerfile
  requirements.txt
  templates/index.html
geocoding-service/
  app.py
  Dockerfile
  requirements.txt
weather-service/
  app.py
  Dockerfile
  requirements.txt
docs/
  screenshots/
report/
  notes.md
```

## What I Learned

- How to split one application flow into small services with clear responsibilities.
- How Docker Compose can connect services through internal service names.
- How a web-facing service can orchestrate calls to backend services.
- How to add basic health endpoints for manual service checks.
- How to handle external API failures without exposing raw errors to users.

## Future Improvements

- Add automated tests for service endpoints and failure cases.
- Add request logging and more structured error messages.
- Add frontend screenshots to `docs/screenshots/` after reviewing them for personal data.
- Add deployment notes for a cloud platform that supports Docker Compose or separate containers.
- Add caching or rate-limit handling for repeated city lookups.

## Notes

- This is a student project, not a production weather service.
- No API keys are stored in the repository.
- Automated tests are not included; use the syntax and smoke checks above for lightweight verification.
