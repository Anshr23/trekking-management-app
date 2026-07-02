from flask import Flask, render_template, request, redirect, url_for, flash
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


# @app.route("/")
# def home():
#     return "Trekking Management Application is running!"
@app.route("/")
def home():
    return render_template("base.html")



# register.html
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        contact = request.form["contact"]
        role = request.form["role"]
        experience = request.form["experience"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        if role not in ["user", "staff"]:
            flash("Invalid role selected.", "danger")
            return redirect(url_for("register"))

        if role == "user":
            approved = True
        else:
            approved = False

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role,
            contact=contact,
            is_approved=approved,
            is_blacklisted=False
        )

        db.session.add(new_user)
        db.session.commit()

        if role == "staff":
            staff_profile = StaffProfile(
                user_id=new_user.id,
                experience=experience
            )

            db.session.add(staff_profile)
            db.session.commit()

            flash(
                "Registration successful. Wait for admin approval before logging in.",
                "success"
            )

        else:
            flash("Registration successful. You can now log in.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")



# login.html
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)