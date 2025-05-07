from fastapi import FastAPI, HTTPException
import swisseph as swe
from datetime import datetime

app = FastAPI()

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
        "true_node": swe.TRUE_NODE
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