
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/<name>")
def welcome(name):
    return render_template("welcome.html", name=name)

@app.route("/about")
def about():
    sites = ['twitter', 'facebook', 'instagram']
    return render_template("about.html", sites=sites)

if __name__ == "__main__":
    app.run()