import hashlib
import base64
from datetime import datetime
import os
import yagmail
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Load environment variables
load_dotenv()

# Setup Fernet
fernet = Fernet(os.getenv("FERNET_KEY").encode())

def generate_otp():
    """
    Generate a 6-character alphanumeric OTP based on UTC time (10s granularity).
    """
    now = datetime.utcnow()
    rounded_seconds = now.second - (now.second % 10)
    timestamp_str = now.strftime(f"%Y%m%d%H%M") + f"{rounded_seconds:02d}"
    raw = timestamp_str.encode()
    otp = base64.b32encode(hashlib.sha256(raw).digest()).decode()[:6]
    return otp  # Example: "K93LE3"

def encrypt_otp(otp):
    return fernet.encrypt(otp.encode()).decode()

def decrypt_otp(ciphertext):
    return fernet.decrypt(ciphertext.encode()).decode()

def send_otp_via_email(email, otp):
    """
    Send the OTP to the given email using Gmail SMTP.
    """
    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASS")
    
    if not user or not password:
        raise RuntimeError("Missing Gmail credentials in .env")

    yag = yagmail.SMTP(user, password)
    yag.send(
        to=email,
        subject="Your OTP ;)",
        contents=f"Your one-time password (OTP) is: {otp}"
    )
