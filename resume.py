# Smart Resume Builder using Flask + MySQL + PDF Download
# Install first:
# pip install flask flask-mysqldb reportlab werkzeug

from flask import Flask, render_template_string, request, redirect, session, send_file
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.secret_key = "secretkey123"

# ---------------- MYSQL CONFIG ----------------
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "resume_builder"

mysql = MySQL(app)

# ---------------- CREATE DATABASE ----------------
"""
Run this in MySQL:

CREATE DATABASE resume_builder;

USE resume_builder;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255)
);

CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    fullname VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    skills TEXT,
    education TEXT,
    experience TEXT,
    template VARCHAR(50)
);
"""

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
                    (username, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect("/login")

    return render_template_string("""
    <h2>Register</h2>
    <form method="post">
    Username:<input type="text" name="username"><br>
    Email:<input type="email" name="email"><br>
    Password:<input type="password" name="password"><br>
    <input type="submit" value="Register">
    </form>
    <a href='/login'>Login</a>
    """)

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/dashboard")

    return render_template_string("""
    <h2>Login</h2>
    <form method="post">
    Email:<input type="email" name="email"><br>
    Password:<input type="password" name="password"><br>
    <input type="submit" value="Login">
    </form>
    <a href='/register'>Register</a>
    """)

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return render_template_string("""
    <h2>Welcome {{name}}</h2>
    <a href='/resume'>Create Resume</a><br>
    <a href='/logout'>Logout</a>
    """, name=session["username"])

# ---------------- RESUME FORM ----------------
@app.route("/resume", methods=["GET", "POST"])
def resume():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        skills = request.form["skills"]
        education = request.form["education"]
        experience = request.form["experience"]
        template = request.form["template"]

        cur = mysql.connection.cursor()
        cur.execute("""
        INSERT INTO resumes(user_id,fullname,phone,email,skills,education,experience,template)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """, (session["user_id"], fullname, phone, email, skills,
              education, experience, template))
        mysql.connection.commit()
        cur.close()

        return redirect("/preview")

    return render_template_string("""
    <h2>Create Resume</h2>
    <form method="post">
    Full Name:<input type="text" name="fullname"><br>
    Phone:<input type="text" name="phone"><br>
    Email:<input type="email" name="email"><br>
    Skills:<textarea name="skills"></textarea><br>
    Education:<textarea name="education"></textarea><br>
    Experience:<textarea name="experience"></textarea><br>

    Template:
    <select name="template">
      <option>Professional</option>
      <option>Modern</option>
      <option>Minimal</option>
    </select><br><br>

    <input type="submit" value="Generate Resume">
    </form>
    """)

# ---------------- PREVIEW ----------------
@app.route("/preview")
def preview():
    if "user_id" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM resumes WHERE user_id=%s ORDER BY id DESC LIMIT 1",
                (session["user_id"],))
    data = cur.fetchone()
    cur.close()

    return render_template_string("""
    <h2>Resume Preview</h2>
    <h3>{{d[2]}}</h3>
    <p>Phone: {{d[3]}}</p>
    <p>Email: {{d[4]}}</p>
    <p><b>Skills:</b> {{d[5]}}</p>
    <p><b>Education:</b> {{d[6]}}</p>
    <p><b>Experience:</b> {{d[7]}}</p>
    <p><b>Template:</b> {{d[8]}}</p>

    <a href='/download'>Download PDF</a><br>
    <a href='/resume'>Edit Resume</a>
    """, d=data)

# ---------------- PDF DOWNLOAD ----------------
@app.route("/download")
def download():
    if "user_id" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM resumes WHERE user_id=%s ORDER BY id DESC LIMIT 1",
                (session["user_id"],))
    data = cur.fetchone()
    cur.close()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "Resume")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 760, f"Name: {data[2]}")
    pdf.drawString(50, 740, f"Phone: {data[3]}")
    pdf.drawString(50, 720, f"Email: {data[4]}")
    pdf.drawString(50, 700, f"Skills: {data[5]}")
    pdf.drawString(50, 680, f"Education: {data[6]}")
    pdf.drawString(50, 660, f"Experience: {data[7]}")

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="resume.pdf",
                     mimetype="application/pdf")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)