
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
import transit_tracker

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/<name>")
def welcome(name):
    return render_template("welcome.html", name=name)

@app.route("/about")
def about():
    sites = ['twitter', 'facebook', 'instagram']
    return render_template("about.html", sites=sites)

@app.route("/home")
def home():
    input_list = [3977, 11504]
    results = transit_tracker.lookup(input_list)
    return render_template("home.html", results=results)

@app.route("/work")
def work():
    input_list = [7789, 13123]
    results = transit_tracker.lookup(input_list)
    return render_template("work.html", results=results)


if __name__ == "__main__":
    app.run()