from flask_sqlalchemy import SQLAlchemy

# Database instance shared across the application
db = SQLAlchemy()


# User model representing the users table
class User(db.Model):

    # Primary key identifier
    id = db.Column(db.Integer, primary_key=True)

    # Unique username for authentication
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Stored hashed password (never store plaintext passwords)
    password_hash = db.Column(db.String(255), nullable=False)