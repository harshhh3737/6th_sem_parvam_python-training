# Online Job Portal (Mini LinkedIn)
# Features:
# - User Registration (Job Seeker / Recruiter)
# - Role Based Login
# - Post Jobs
# - Apply Jobs
# - Track Applications
# - REST APIs
# - Resume Upload
# - Job Search / Filtering
# Run:
# pip install flask flask_sqlalchemy werkzeug

import os
from datetime import datetime
from flask import Flask, request, jsonify, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# ---------------- APP CONFIG ---------------- #

app = Flask(__name__)
app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobportal.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# ---------------- DATABASE MODELS ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))   # seeker / recruiter
    resume = db.Column(db.String(200), nullable=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    skills = db.Column(db.String(200))
    recruiter_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seeker_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    status = db.Column(db.String(30), default="Applied")
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- HELPERS ---------------- #

def current_user():
    uid = session.get("user_id")
    if uid:
        return User.query.get(uid)
    return None

def login_required():
    user = current_user()
    if not user:
        return None
    return user

# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["POST"])
def register():
    data = request.form

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role=data["role"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered Successfully"})

# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["POST"])
def login():
    data = request.form
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        session["user_id"] = user.id
        session["role"] = user.role
        return jsonify({
            "message": "Login Success",
            "role": user.role
        })

    return jsonify({"error": "Invalid credentials"}), 401

# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged Out"})

# ---------------- POST JOB ---------------- #

@app.route("/post_job", methods=["POST"])
def post_job():
    user = login_required()
    if not user:
        return jsonify({"error": "Login required"}), 401

    if user.role != "recruiter":
        return jsonify({"error": "Only recruiters can post jobs"}), 403

    data = request.form

    job = Job(
        title=data["title"],
        company=data["company"],
        location=data["location"],
        salary=data["salary"],
        skills=data["skills"],
        recruiter_id=user.id
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({"message": "Job Posted Successfully"})

# ---------------- LIST / FILTER JOBS ---------------- #

@app.route("/jobs", methods=["GET"])
def jobs():
    keyword = request.args.get("keyword", "")
    location = request.args.get("location", "")

    query = Job.query

    if keyword:
        query = query.filter(
            Job.title.contains(keyword) |
            Job.skills.contains(keyword)
        )

    if location:
        query = query.filter(Job.location.contains(location))

    all_jobs = query.order_by(Job.created_at.desc()).all()

    result = []
    for j in all_jobs:
        result.append({
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "salary": j.salary,
            "skills": j.skills
        })

    return jsonify(result)

# ---------------- APPLY JOB ---------------- #

@app.route("/apply/<int:job_id>", methods=["POST"])
def apply(job_id):
    user = login_required()
    if not user:
        return jsonify({"error": "Login required"}), 401

    if user.role != "seeker":
        return jsonify({"error": "Only seekers can apply"}), 403

    already = Application.query.filter_by(
        seeker_id=user.id,
        job_id=job_id
    ).first()

    if already:
        return jsonify({"error": "Already applied"}), 400

    app_obj = Application(
        seeker_id=user.id,
        job_id=job_id
    )

    db.session.add(app_obj)
    db.session.commit()

    return jsonify({"message": "Applied Successfully"})

# ---------------- TRACK APPLICATIONS ---------------- #

@app.route("/my_applications")
def my_applications():
    user = login_required()
    if not user:
        return jsonify({"error": "Login required"}), 401

    if user.role != "seeker":
        return jsonify({"error": "Only seekers allowed"}), 403

    apps = Application.query.filter_by(seeker_id=user.id).all()

    result = []
    for a in apps:
        job = Job.query.get(a.job_id)

        result.append({
            "job_title": job.title,
            "company": job.company,
            "status": a.status,
            "applied_at": a.applied_at.strftime("%Y-%m-%d %H:%M")
        })

    return jsonify(result)

# ---------------- RECRUITER VIEW APPLICANTS ---------------- #

@app.route("/job_applications/<int:job_id>")
def job_applications(job_id):
    user = login_required()
    if not user:
        return jsonify({"error": "Login required"}), 401

    job = Job.query.get_or_404(job_id)

    if user.role != "recruiter" or job.recruiter_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    apps = Application.query.filter_by(job_id=job_id).all()

    result = []
    for a in apps:
        seeker = User.query.get(a.seeker_id)

        result.append({
            "name": seeker.name,
            "email": seeker.email,
            "resume": seeker.resume,
            "status": a.status
        })

    return jsonify(result)

# ---------------- RESUME UPLOAD ---------------- #

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    user = login_required()
    if not user:
        return jsonify({"error": "Login required"}), 401

    if user.role != "seeker":
        return jsonify({"error": "Only seekers allowed"}), 403

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    filename = secure_filename(file.filename)

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    user.resume = filename
    db.session.commit()

    return jsonify({"message": "Resume Uploaded"})

# ---------------- DOWNLOAD RESUME ---------------- #

@app.route("/resume/<filename>")
def resume(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)