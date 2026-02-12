from flask import Flask, render_template, request
import os, sqlite3, uuid
import PyPDF2, docx

from resume_logic import resume_analysis
from mailer import send_mail

BASE_URL = "https://yuonne-unulcerous-daphine.ngrok-free.dev"

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    return sqlite3.connect("database.db")

def extract_text(path):
    text = ""

    if path.lower().endswith(".pdf"):
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""

    elif path.lower().endswith(".docx"):
        doc = docx.Document(path)
        for para in doc.paragraphs:
            text += para.text + " "

    return text


# ---------------- RESUME UPLOAD ----------------
@app.route("/", methods=["GET", "POST"])
def resume_upload():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        resume = request.files["resume"]

        path = os.path.join(UPLOAD_FOLDER, resume.filename)
        resume.save(path)

        text = extract_text(path)
        phase1_result = resume_analysis(text)

        status = "shortlisted" if phase1_result["decision"] == "Shortlisted" else "rejected"

        db = get_db()
        db.execute("""
        INSERT OR REPLACE INTO candidates
        (name, email, resume_path, status)
        VALUES (?, ?, ?, ?)
        """, (name, email, path, status))
        db.commit()
        db.close()

        return render_template("result.html", result=phase1_result, email=email)

    return render_template("resume_upload.html")


# ---------------- CALENDAR ----------------
@app.route("/calendar/<email>", methods=["GET", "POST"])
def calendar(email):

    if request.method == "POST":

        date = request.form["date"]
        token = str(uuid.uuid4())
        link = f"{BASE_URL}/interview/{token}"

        db = get_db()

        # 🔹 Fetch candidate name from DB
        cur = db.execute("SELECT name FROM candidates WHERE email=?", (email,))
        row = cur.fetchone()

        if row:
            name = row[0]
        else:
            name = "Candidate"

        # 🔹 Update interview details
        db.execute("""
            UPDATE candidates
            SET interview_date=?, interview_link=?, interview_token=?
            WHERE email=?
        """, (date, link, token, email))

        db.commit()
        db.close()

        # 🔹 Send email with candidate name
        send_mail(name, email, link, date)

        return render_template("success.html")

    return render_template("calendar.html")


# ---------------- INTERVIEW ----------------
@app.route("/interview/<token>")
def interview(token):
    db = get_db()
    cur = db.execute("""
    SELECT name, resume_path FROM candidates
    WHERE interview_token=?
    """, (token,))
    user = cur.fetchone()
    db.close()

    if not user:
        return "Invalid or expired interview link"

    return render_template("interview.html", name=user[0], resume=user[1])


if __name__ == "__main__":
    app.run(debug=True)
