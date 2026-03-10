from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

# Import database instance and User model
from models import db, User


# Initialize Flask application
app = Flask(__name__)

# Secret key used to sign session cookies
app.secret_key = "secret-key"


# Database configuration (SQLite file stored in project directory)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# Disable modification tracking to reduce overhead
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize SQLAlchemy with the Flask app
db.init_app(app)


# Create database tables if they do not already exist
with app.app_context():
    db.create_all()


# Home route
@app.route("/")
def home():
    return render_template("home.html")


# Login route handling both page rendering and authentication
@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    # Process form submission
    if request.method == "POST":

        # Retrieve submitted credentials
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        # Validate password against stored hash
        if user and check_password_hash(user.password_hash, password):

            # Persist authenticated user in session
            session["username"] = user.username

            return redirect(url_for("dashboard"))

        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)


# Protected dashboard route
@app.route("/dashboard")
def dashboard():

    # Ensure user is authenticated before allowing access
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])


# Logout route
@app.route("/logout")
def logout():

    # Remove authenticated user from session
    session.pop("username", None)

    return redirect(url_for("login"))


# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Basic validation
        if not username or not password:
            error = "Username and password are required."
        elif len(username) < 3:
            error = "Username must be at least 3 characters long."
        elif len(password) < 8:
            error = "Password must be at least 8 characters long."
        else:
            # Check whether the username already exists
            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                error = "Username already exists."
            else:
                # Create a new user with a hashed password
                new_user = User(
                    username=username,
                    password_hash=generate_password_hash(password)
                )

                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for("login"))

    return render_template("register.html", error=error)


# Run Flask development server
if __name__ == "__main__":
    app.run(debug=True)