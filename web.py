from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #hard coded credentials for testing and monitering versios 1
        if username == "knight" and password == "password123":
            return render_template("dashboard.html", username=username)
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", username="alice")

if __name__ == "__main__":
    app.run(debug=True)