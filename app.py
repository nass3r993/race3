from flask import Flask, render_template, request, redirect, session, url_for
from dotenv import load_dotenv
from otp_utils import generate_otp, send_otp_via_email, encrypt_otp, decrypt_otp
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        otp = generate_otp()
        send_otp_via_email(email, otp)
        session["email"] = email
        session["otp"] = encrypt_otp(otp)  # Store encrypted OTP
        return redirect(url_for("verify"))
    return render_template("login.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        otp_input = request.form["otp"]
        email = session.get("email")
        enc_otp = session.get("otp")
        if email and enc_otp and otp_input == decrypt_otp(enc_otp):
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        return "Invalid OTP"
    return render_template("verify.html")


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if session.get("email") == "ad0min3333@gmail.com":
        return render_template("dashboard.html", flag="Nass3r000{Solved_th3_Lab}")
    return render_template("dashboard.html", flag=None)


if __name__ == "__main__":
    app.run(debug=False)
