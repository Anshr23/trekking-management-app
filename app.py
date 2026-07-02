from flask import Flask
from werkzeug.security import generate_password_hash
from models import db, User, StaffProfile, Trek, Booking

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SECRET_KEY"] = "trekking-secret-key"

db.init_app(app)


with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email="admin@tma.com").first()

    if not admin:
        admin = User(
            name="Admin",
            email="admin@tma.com",
            password=generate_password_hash("admin123"),
            role="admin",
            is_approved=True,
            is_blacklisted=False
        )

        db.session.add(admin)
        db.session.commit()

        print("Default admin created successfully!")


@app.route("/")
def home():
    return "Trekking Management Application is running!"


if __name__ == "__main__":
    app.run(debug=True)