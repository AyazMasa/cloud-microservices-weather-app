# Cloud Second Project: Weather Lookup SOA

## Problem Statement

The project demonstrates a small service-oriented cloud application. A user enters a city name, and the system validates the location, retrieves coordinates, requests weather data, and displays the result in a browser.

## Architecture Summary

- `webapp`: Flask browser interface on port `5000` inside Docker, exposed as `localhost:8080`.
- `geocoding-service`: Flask API on port `5001`, uses Nominatim to convert a city name to latitude and longitude.
- `weather-service`: Flask API on port `5002`, uses Open-Meteo to return current weather and a 3-day forecast.
- Docker Compose connects the three services on one internal network.

```text
Browser -> webapp -> geocoding-service -> Nominatim
                |
                +-> weather-service ----> Open-Meteo
```

## Input / Processing / Output

- Input: city name from the web form.
- Processing: geocoding service validates the city and returns coordinates; weather service uses coordinates to request weather data.
- Output: formatted location name, current temperature, current wind speed, and a 3-day forecast.

## Suggested Screenshots

- Docker Compose running the three containers.
- Browser page before entering a city.
- Successful result for a valid city.
- Friendly error for an invalid city.
- Curl test for `/health`, `/geocode`, and `/forecast`.

## Suggested Test Cases

- Valid city: `Kyiv`, `London`, or `Paris`.
- Invalid city: random text such as `asdfgh-city`.
- Missing city input: submit an empty form or call `/geocode` without `city`.
- Geocoding service failure: stop or block `geocoding-service`.
- Weather service failure: stop or block `weather-service`.

## Work Split for Two Students

- Student 1: webapp, HTML template, Docker Compose, README run instructions.
- Student 2: geocoding service, weather service, API testing, report notes.
- Shared: final integration testing, screenshots, presentation practice.

## Written Report Sections

1. Introduction
2. Problem Statement
3. System Architecture
4. Service Descriptions
5. Docker Compose Configuration
6. Data Flow
7. Testing and Results
8. Error Handling
9. Work Distribution
10. Conclusion

## 10-Slide Presentation Outline

1. Project title and team members
2. Problem and goal
3. Requirements
4. System architecture diagram
5. Webapp service
6. Geocoding service
7. Weather service
8. Docker Compose setup
9. Demo and test cases
10. Conclusion and possible improvements
