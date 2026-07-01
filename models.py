from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    contact = db.Column(db.String(20))
    is_approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)

    bookings = db.relationship("Booking", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"


class StaffProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=True,
        nullable=False
    )

    experience = db.Column(db.String(200))

    user = db.relationship(
        "User",
        backref=db.backref("staff_profile", uselist=False)
    )

    def __repr__(self):
        return f"<StaffProfile {self.id}>"


class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)

    assigned_staff_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    status = db.Column(db.String(20), default="Pending")
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    assigned_staff = db.relationship(
        "User",
        foreign_keys=[assigned_staff_id],
        backref="assigned_treks"
    )

    bookings = db.relationship("Booking", backref="trek", lazy=True)

    def __repr__(self):
        return f"<Trek {self.name}>"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("trek.id"),
        nullable=False
    )

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        default="Booked"
    )

    def __repr__(self):
        return f"<Booking {self.id}>"