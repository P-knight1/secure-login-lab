from werkzeug.security import generate_password_hash

from app import app
from models import db, User


# Run within application context to access database
with app.app_context():

    # Prevent duplicate creation of the test user
    existing_user = User.query.filter_by(username="alice").first()

    if not existing_user:

        # Create initial test user
        user = User(
            username="alice",
            password_hash=generate_password_hash("Password123")
        )

        # Persist user to the database
        db.session.add(user)
        db.session.commit()

        print("Test user 'alice' created.")

    else:
        print("User 'alice' already exists.")