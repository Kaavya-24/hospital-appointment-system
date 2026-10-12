import os
import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
DATABASE = os.path.join(app.root_path, "data", "hospital.db")

DOCTORS = [
    {"id": 1, "name": "Dr. Ananya Sharma", "specialty": "Cardiology", "time": "Mon–Fri"},
    {"id": 2, "name": "Dr. Rahul Menon", "specialty": "Dermatology", "time": "Mon–Sat"},
    {"id": 3, "name": "Dr. Priya Nair", "specialty": "Pediatrics", "time": "Tue–Sat"},
    {"id": 4, "name": "Dr. Arjun Kumar", "specialty": "Orthopedics", "time": "Mon–Fri"},
]

def get_db():
    if "db" not in g:
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            reason TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()

@app.route("/")
def index():
    with app.app_context():
        init_db()
    return render_template("index.html", doctors=DOCTORS, today=date.today().isoformat())

@app.route("/book", methods=["POST"])
def book():
    patient_name = request.form.get("patient_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    reason = request.form.get("reason", "").strip()
    appointment_date = request.form.get("appointment_date", "").strip()

    try:
        doctor_id = int(request.form.get("doctor_id", ""))
    except ValueError:
        doctor_id = -1

    if not all([patient_name, email, phone, reason, appointment_date]):
        flash("Please complete every field.", "error")
        return redirect(url_for("index"))

    if "@" not in email or "." not in email.split("@")[-1]:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("index"))

    if not phone.isdigit() or len(phone) < 10 or len(phone) > 15:
        flash("Enter a phone number containing 10–15 digits.", "error")
        return redirect(url_for("index"))

    if doctor_id not in [doctor["id"] for doctor in DOCTORS]:
        flash("Please select a valid doctor.", "error")
        return redirect(url_for("index"))

    try:
        selected_date = date.fromisoformat(appointment_date)
        if selected_date < date.today():
            flash("Appointment date cannot be in the past.", "error")
            return redirect(url_for("index"))
    except ValueError:
        flash("Please enter a valid appointment date.", "error")
        return redirect(url_for("index"))

    db = get_db()
    db.execute("""
        INSERT INTO appointments
        (patient_name, email, phone, doctor_id, appointment_date, reason)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (patient_name, email, phone, doctor_id, appointment_date, reason))
    db.commit()

    flash("Appointment request submitted successfully!", "success")
    return redirect(url_for("appointments"))

@app.route("/appointments")
def appointments():
    db = get_db()
    rows = db.execute("""
        SELECT id, patient_name, email, phone, doctor_id,
               appointment_date, reason, created_at
        FROM appointments
        ORDER BY appointment_date, id DESC
    """).fetchall()

    doctor_map = {doctor["id"]: doctor for doctor in DOCTORS}
    records = []
    for row in rows:
        item = dict(row)
        item["doctor_name"] = doctor_map.get(item["doctor_id"], {}).get("name", "Unknown")
        item["specialty"] = doctor_map.get(item["doctor_id"], {}).get("specialty", "")
        records.append(item)

    return render_template("appointments.html", appointments=records)

@app.route("/health")
def health():
    return {"status": "ok", "service": "hospital-appointment-system"}, 200

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
