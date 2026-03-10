# Flask imports for routing, templates, request handling, sessions, and redirects
from flask import Flask, render_template, request, session, redirect, url_for

# Werkzeug utilities for secure password hashing and verification
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask application
app = Flask(__name__)

# Secret key used to sign session cookies
app.secret_key = "secret-key"


# Temporary in-memory user store (placeholder for a database)
users = {
    "alice": {
        "password_hash": generate_password_hash("Password123")
    }
}


# Home route
@app.route("/")
def home():
    return render_template("home.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        # Retrieve submitted form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Look up user in the in-memory store
        user = users.get(username)

        # Verify password against stored hash
        if user and check_password_hash(user["password_hash"], password):
            # Persist authenticated user in session
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)


# Protected dashboard route
@app.route("/dashboard")
def dashboard():
    # Require authentication
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])


# Logout route
@app.route("/logout")
def logout():
    # Remove user from session
    session.pop("username", None)
    return redirect(url_for("login"))


# Run development server
if __name__ == "__main__":
    app.run(debug=True)