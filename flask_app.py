
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5

import config
import transit_tracker
import weather_tracker

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    sites = ['twitter', 'facebook', 'instagram']
    return render_template("about.html", sites=sites)

@app.route("/transit/")
def transit():
    return render_template("transit.html")

@app.route("/transit/home")
def transithome():
    input_list = [3977, 11504]
    results = transit_tracker.lookup(input_list)
    return render_template("transithome.html", results=results)

@app.route("/transit/work")
def transitwork():
    input_list = [7789, 13123]
    results = transit_tracker.lookup(input_list)
    return render_template("transitwork.html", results=results)

@app.route("/transit/moda")
def transitmoda():
    input_list = [1097, 11508]
    results = transit_tracker.lookup(input_list)
    return render_template("transitmoda.html", results=results)

@app.route("/weather/")
def weather():
    query = (request.args.get("q") or "").strip()[:100]
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    label = (request.args.get("name") or "").strip()
    error, matches, timezone = None, [], "auto"

    if lat is not None and lon is not None:
        coords = [max(-90, min(90, lat)), max(-180, min(180, lon))]
    elif query:
        try:
            matches = weather_tracker.geocode_location(query)
        except Exception:
            matches = []
            error = "Location search is unavailable right now."
        if matches:
            top = matches[0]
            coords = [top["latitude"], top["longitude"]]
            timezone = top["timezone"]
            label = ", ".join(p for p in (top["name"], top["region"], top["country"]) if p)
        else:
            coords = None
            error = error or f'No location found for "{query}".'
    else:
        coords, label = [45.55, -122.69], "Portland, OR, US"

    report = None
    if coords:
        try:
            report = weather_tracker.get_hourly_weather_data(coords, timezone=timezone)
        except Exception:
            error = "Weather data is unavailable right now."

    return render_template(
        "weather.html",
        weather_report=report,
        query=query,
        place=label,
        matches=matches[1:],
        error=error,
    )


if __name__ == "__main__":
    app.run()