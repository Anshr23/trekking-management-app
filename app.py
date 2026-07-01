from flask import Flask
from models import db, User, StaffProfile, Trek, Booking

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SECRET_KEY"] = "trekking-secret-key"

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Trekking Management Application is running!"


if __name__ == "__main__":
    app.run(debug=True)