from fastapi import FastAPI, HTTPException
import swisseph as swe
from datetime import datetime

app = FastAPI(servers=[{"url": "http://92.243.25.184:8000"}])

@app.get("/planet/{planet}/{year}/{month}/{day}")
def planet_position(planet: str, year: int, month: int, day: int):
    planets = {
        "sun": swe.SUN,
        "moon": swe.MOON,
        "mercury": swe.MERCURY,
        "venus": swe.VENUS,
        "mars": swe.MARS,
        "jupiter": swe.JUPITER,
        "saturn": swe.SATURN,
        "uranus": swe.URANUS,
        "neptune": swe.NEPTUNE,
        "pluto": swe.PLUTO,
        "mean_node": swe.MEAN_NODE,
        "true_node": swe.TRUE_NODE,
        "chiron": swe.CHIRON,
        "lilith": swe.MEAN_APOG,  # Mean Black Moon Lilith
        "ceres": swe.CERES,
        "vesta": swe.VESTA,
        "juno": swe.JUNO,
        "pallas": swe.PALLAS
    }

    planet = planet.lower()
    if planet not in planets:
        raise HTTPException(status_code=404, detail="Planet not recognized")

    jd_ut = swe.julday(year, month, day)
    position, ret = swe.calc_ut(jd_ut, planets[planet])

    return {
        "planet": planet,
        "date": f"{year}-{month:02d}-{day:02d}",
        "longitude": position[0],
        "latitude": position[1],
        "distance": position[2]
    }
@app.get("/houses/{year}/{month}/{day}/{hour}/{minute}/{lat}/{lon}")
def calculate_houses(year: int, month: int, day: int, hour: int, minute: int, lat: float, lon: float):
    jd_ut = swe.julday(year, month, day, hour + minute / 60.0)
    houses, asc_mc = swe.houses(jd_ut, lat, lon, b'A')
    return {
        "ascendant": asc_mc[0],
        "mc": asc_mc[1],
        "houses": houses
    }

@app.get("/aspects/{planet1}/{planet2}/{year}/{month}/{day}")
def calculate_aspect(planet1: str, planet2: str, year: int, month: int, day: int):
    planet_ids = {
        "sun": swe.SUN, "moon": swe.MOON, "mercury": swe.MERCURY,
        "venus": swe.VENUS, "mars": swe.MARS, "jupiter": swe.JUPITER,
        "saturn": swe.SATURN, "uranus": swe.URANUS, "neptune": swe.NEPTUNE,
        "pluto": swe.PLUTO, "chiron": swe.CHIRON, "lilith": swe.MEAN_APOG,
        "ceres": swe.CERES, "vesta": swe.VESTA, "juno": swe.JUNO,
        "pallas": swe.PALLAS, "mean_node": swe.MEAN_NODE, "true_node": swe.TRUE_NODE
    }

    jd_ut = swe.julday(year, month, day)
    pos1, _ = swe.calc_ut(jd_ut, planet_ids[planet1.lower()])
    pos2, _ = swe.calc_ut(jd_ut, planet_ids[planet2.lower()])

    aspect_angle = abs(pos1[0] - pos2[0])
    if aspect_angle > 180:
        aspect_angle = 360 - aspect_angle

    return {
        "planet1": planet1,
        "planet2": planet2,
        "date": f"{year}-{month:02d}-{day:02d}",
        "aspect_angle": aspect_angle
    }