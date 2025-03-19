from flask import Flask, render_template, request, send_file, session, redirect, url_for
from flask_mail import Mail, Message
import os
from detect import detect_potholes
from generate_report import generate_report



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-app-password'  # Use an app password, not your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)

UPLOAD_FOLDER = "uploads"
DETECTION_FOLDER = "static/detections"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECTION_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    detection_message = None
    report_path = None

    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Check if file is image or video
            is_video = filename.lower().endswith((".mp4", ".avi", ".mov"))

            # Detect potholes
            detected_path, detections = detect_potholes(file_path, is_video)

            if detections and len(detections) > 0:
                detection_message = "🚧 Pothole Detected!"
                report_path = generate_report(detections, detected_path)
                
                # Send report via email
                if "email" in session:
                    send_report_email(session["email"], report_path)
            else:
                detection_message = "✅ No Pothole Found!"

            return render_template("index.html", detected_path=detected_path, report_path=report_path, detection_message=detection_message)

    return render_template("index.html", detection_message=detection_message)

def send_report_email(email, report_path):
    """Sends the generated report to the user's email."""
    try:
        msg = Message("Pothole Detection Report", recipients=[email])
        msg.body = "Attached is your pothole detection report."
        with app.open_resource(report_path) as pdf:
            msg.attach("pothole_report.pdf", "application/pdf", pdf.read())

        mail.send(msg)
        print(f"✅ Report sent to {email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Simple login system for testing."""
    if request.method == "POST":
        session["email"] = request.form["email"]
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Logs out the user."""
    session.pop("email", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
