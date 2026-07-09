# Trekking Management Application (TMA)

Trekking Management Application is a role-based web application developed as part of the IIT Madras BS Degree MAD-I project.

The application allows administrators, trek staff, and trekkers to manage trekking activities, staff assignments, participant bookings, trek availability, and trekking history.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Jinja2
- HTML
- CSS
- Bootstrap
- Chart.js

## User Roles

### Admin
- View application statistics
- Create, edit, and delete treks
- Approve and manage trek staff
- Manage and blacklist users
- Assign staff to treks
- View all bookings
- Search users, staff, and treks
- View trekking statistics and charts

### Trek Staff
- Register and log in after admin approval
- View assigned treks
- Update available slots and trek status
- View registered participants
- Mark treks as started or completed
- Edit staff profile

### Trekker
- Register and log in
- View available open treks
- Search and filter treks
- Book and cancel trek bookings
- View booking status and trekking history
- Edit profile

## Additional Features

- Role-based access control
- Password hashing
- Prevention of overbooking
- Booking history maintenance
- JSON API endpoints using GET, POST, PUT, and DELETE
- Admin statistics and data visualizations
- Responsive Bootstrap interface

## Database

The application uses SQLite. The database and all required tables are created programmatically when the application starts.

The default administrator account is also created automatically.

Default Admin Credentials:

- Email: `admin@tma.com`
- Password: `admin123`

## Installation and Running

Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate
Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

Open the application at:

http://127.0.0.1:5000

Database Models

The application contains four main database models:

User
StaffProfile
Trek
Booking

These models are connected using SQLAlchemy relationships and foreign keys.

API Endpoints

The application provides JSON API endpoints for:

Retrieving treks
Retrieving individual trek details
Creating treks
Updating treks
Deleting treks
Retrieving users
Retrieving bookings

Modifying trek data through the API requires Admin authentication.

Project Structure
trekking-management-app/
├── app.py
├── models.py
├── requirements.txt
├── README.md
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── admin/
    ├── staff/
    └── user/
Author

Ansh Rai