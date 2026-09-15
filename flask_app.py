
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import transit_tracker

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    sites = ['twitter', 'facebook', 'instagram']
    return render_template("about.html", sites=sites)

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


if __name__ == "__main__":
    app.run()