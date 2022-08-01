from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/spec_1")
def spec_1():
    return render_template("spec_1.html")

@app.route("/spec_2")
def spec_2():
    return render_template("spec_2.html")

@app.route("/spec_3")
def spec_3():
    return render_template("spec_3.html")

@app.route("/spec_4")
def spec_4():
    return render_template("spec_4.html")

if __name__ == "__main__":
    app.run(debug=True)
