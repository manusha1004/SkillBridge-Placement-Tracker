from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-for-production"
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "skillbridge.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied',
                applied_on DATE DEFAULT CURRENT_DATE
            )
        """)
        if conn.execute("SELECT COUNT(*) FROM goals").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO goals (title, category, status) VALUES (?, ?, ?)",
                [
                    ("Practice 5 Java problems", "Coding", "In Progress"),
                    ("Revise SQL joins", "Database", "Pending"),
                    ("Update resume", "Career", "Completed"),
                ],
            )
        if conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO applications (company, role, status) VALUES (?, ?, ?)",
                [
                    ("Example Technologies", "Software Intern", "Applied"),
                    ("Sample Systems", "Graduate Trainee", "Preparing"),
                ],
            )

@app.route("/")
def dashboard():
    with get_db() as conn:
        goals = conn.execute("SELECT * FROM goals ORDER BY id DESC").fetchall()
        applications = conn.execute("SELECT * FROM applications ORDER BY id DESC").fetchall()
        total_goals = conn.execute("SELECT COUNT(*) FROM goals").fetchone()[0]
        completed = conn.execute("SELECT COUNT(*) FROM goals WHERE status='Completed'").fetchone()[0]
        total_apps = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    progress = round((completed / total_goals) * 100) if total_goals else 0
    return render_template("dashboard.html", goals=goals, applications=applications,
                           total_goals=total_goals, completed=completed,
                           total_apps=total_apps, progress=progress)

@app.route("/goals/add", methods=["POST"])
def add_goal():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "Other").strip()
    if not title:
        flash("Please enter a goal title.", "error")
    else:
        with get_db() as conn:
            conn.execute("INSERT INTO goals (title, category) VALUES (?, ?)", (title, category))
        flash("Learning goal added.", "success")
    return redirect(url_for("dashboard"))

@app.route("/goals/<int:goal_id>/status", methods=["POST"])
def update_goal(goal_id):
    status = request.form.get("status", "Pending")
    if status not in {"Pending", "In Progress", "Completed"}:
        status = "Pending"
    with get_db() as conn:
        conn.execute("UPDATE goals SET status=? WHERE id=?", (status, goal_id))
    flash("Goal status updated.", "success")
    return redirect(url_for("dashboard"))

@app.route("/goals/<int:goal_id>/delete", methods=["POST"])
def delete_goal(goal_id):
    with get_db() as conn:
        conn.execute("DELETE FROM goals WHERE id=?", (goal_id,))
    flash("Goal deleted.", "success")
    return redirect(url_for("dashboard"))

@app.route("/applications/add", methods=["POST"])
def add_application():
    company = request.form.get("company", "").strip()
    role = request.form.get("role", "").strip()
    status = request.form.get("status", "Applied")
    if status not in {"Preparing", "Applied", "Assessment", "Interview", "Offer", "Rejected"}:
        status = "Applied"
    if not company or not role:
        flash("Company and role are required.", "error")
    else:
        with get_db() as conn:
            conn.execute("INSERT INTO applications (company, role, status) VALUES (?, ?, ?)",
                         (company, role, status))
        flash("Application added.", "success")
    return redirect(url_for("dashboard"))

@app.route("/applications/<int:application_id>/delete", methods=["POST"])
def delete_application(application_id):
    with get_db() as conn:
        conn.execute("DELETE FROM applications WHERE id=?", (application_id,))
    flash("Application deleted.", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
