from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
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

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No account found with this email.", "danger")
            return redirect(url_for("login"))

        if not check_password_hash(user.password, password):
            flash("Incorrect password.", "danger")
            return redirect(url_for("login"))

        if user.is_blacklisted:
            flash("Your account has been blacklisted. Contact the admin.", "danger")
            return redirect(url_for("login"))

        if user.role == "staff" and not user.is_approved:
            flash("Your staff account is waiting for admin approval.", "warning")
            return redirect(url_for("login"))

        session["user_id"] = user.id
        session["name"] = user.name
        session["role"] = user.role

        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))

        elif user.role == "staff":
            return redirect(url_for("staff_dashboard"))

        else:
            return redirect(url_for("user_dashboard"))

    return render_template("login.html")



#logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))



#admin route
@app.route("/admin/dashboard")
def admin_dashboard():

    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    if session["role"] != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("home"))

    total_treks = Trek.query.count()

    total_users = User.query.filter_by(role="user").count()

    total_staff = User.query.filter_by(role="staff").count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings
    )

@app.route("/admin/treks")
def admin_treks():

    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    if session["role"] != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("home"))

    treks = Trek.query.all()

    return render_template(
        "admin/treks.html",
        treks=treks
    )


@app.route("/admin/treks/add", methods=["GET", "POST"])
def add_trek():

    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    if session["role"] != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("home"))

    approved_staff = User.query.filter_by(
        role="staff",
        is_approved=True,
        is_blacklisted=False
    ).all()

    if request.method == "POST":

        name = request.form["name"]
        location = request.form["location"]
        difficulty = request.form["difficulty"]
        duration = int(request.form["duration"])
        available_slots = int(request.form["available_slots"])
        status = request.form["status"]

        start_date = datetime.strptime(
            request.form["start_date"],
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            request.form["end_date"],
            "%Y-%m-%d"
        ).date()

        staff_id = request.form["assigned_staff_id"]

        if staff_id:
            assigned_staff_id = int(staff_id)
        else:
            assigned_staff_id = None

        if end_date < start_date:
            flash("End date cannot be before start date.", "danger")

            return render_template(
                "admin/trek_form.html",
                trek=None,
                approved_staff=approved_staff
            )

        new_trek = Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            available_slots=available_slots,
            assigned_staff_id=assigned_staff_id,
            status=status,
            start_date=start_date,
            end_date=end_date
        )

        db.session.add(new_trek)
        db.session.commit()

        flash("Trek created successfully.", "success")

        return redirect(url_for("admin_treks"))

    return render_template(
        "admin/trek_form.html",
        trek=None,
        approved_staff=approved_staff
    )


@app.route("/admin/treks/<int:trek_id>/edit", methods=["GET", "POST"])
def edit_trek(trek_id):

    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    if session["role"] != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("home"))

    trek = db.session.get(Trek, trek_id)

    if not trek:
        flash("Trek not found.", "danger")
        return redirect(url_for("admin_treks"))

    approved_staff = User.query.filter_by(
        role="staff",
        is_approved=True,
        is_blacklisted=False
    ).all()

    if request.method == "POST":

        start_date = datetime.strptime(
            request.form["start_date"],
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            request.form["end_date"],
            "%Y-%m-%d"
        ).date()

        if end_date < start_date:
            flash("End date cannot be before start date.", "danger")

            return render_template(
                "admin/trek_form.html",
                trek=trek,
                approved_staff=approved_staff
            )

        trek.name = request.form["name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = int(request.form["duration"])
        trek.available_slots = int(request.form["available_slots"])
        trek.status = request.form["status"]
        trek.start_date = start_date
        trek.end_date = end_date

        staff_id = request.form["assigned_staff_id"]

        if staff_id:
            trek.assigned_staff_id = int(staff_id)
        else:
            trek.assigned_staff_id = None

        db.session.commit()

        flash("Trek updated successfully.", "success")

        return redirect(url_for("admin_treks"))

    return render_template(
        "admin/trek_form.html",
        trek=trek,
        approved_staff=approved_staff
    )


@app.route("/admin/treks/<int:trek_id>/delete", methods=["POST"])
def delete_trek(trek_id):

    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    if session["role"] != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("home"))

    trek = db.session.get(Trek, trek_id)

    if not trek:
        flash("Trek not found.", "danger")
        return redirect(url_for("admin_treks"))

    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully.", "success")

    return redirect(url_for("admin_treks"))




#staff route
@app.route("/staff/dashboard")
def staff_dashboard():

    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    if session["role"] != "staff":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("home"))

    return render_template("staff/dashboard.html")




#user route
@app.route("/user/dashboard")
def user_dashboard():

    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    if session["role"] != "user":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("home"))

    return render_template("user/dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)