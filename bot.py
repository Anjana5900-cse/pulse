import os
import requests
import smtplib
from datetime import datetime
import pytz
from email.mime.text import MIMEText

# --- CONFIGURATION ---
CITY = "Kochi"
API_KEY = "00e7b7285a23a941424fafb95e3f7b7b"  # <-- Paste your real OpenWeatherMap key here
MY_EMAIL = "satheesanjana59@gmail.com"
# ---------------------

def fetch_quote():
    """Fetches the daily inspirational quote required by the project guide"""
    print("Fetching daily quote from ZenQuotes...")
    try:
        response = requests.get("https://zenquotes.io/api/today")
        if response.status_code == 200:
            data = response.json()
            quote = data[0]['q']
            author = data[0]['a']
            return f'"{quote}" — {author}'
    except Exception as e:
        print(f"Could not fetch quote: {e}")
    return '"Keep pushing forward, day by day." — Anonymous'

def check_weather_and_alert():
    # 1. Fetch Core Project Time (IST)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_timezone).strftime("%Y-%m-%d %I:%M:%S %p")
    print(f"Timestamp: {current_time}")

    # 2. Fetch Core Project Quote
    daily_quote = fetch_quote()
    print(f"Quote: {daily_quote}")

    # 3. Fetch Supplementary Weather Data from OpenWeatherMap
    print(f"Fetching live weather for {CITY} from OpenWeatherMap...")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"API Error ({response.status_code}): {response.json().get('message', 'Unknown error')}")
        return

    data = response.json()
    temp = data["main"]["temp"]
    detailed_desc = data["weather"][0]["description"]
    weather_desc = data["weather"][0]["main"].lower()
    
    print(f"Temperature: {temp}°C | Condition: {detailed_desc.capitalize()}")
    
    # Check assignment alert rules (> 35°C OR Rain)
    is_hot = temp > 35
    is_raining = "rain" in weather_desc or "drizzle" in weather_desc

    # 4. Save EVERYTHING beautifully inside daily_summary.txt
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        # --- PROJECT BLOCK ---
        f.write("==================================================\n")
        f.write("PROJECT: DAILY PULSE TASK BOT\n")
        f.write("==================================================\n")
        f.write(f"Run Timestamp : {current_time} (IST)\n")
        f.write(f"Daily Quote   : {daily_quote}\n\n")
        
        # --- TASK BLOCK ---
        f.write("==================================================\n")
        f.write("TASK: OPENWEATHERMAP ALERT\n")
        f.write("==================================================\n")
        f.write(f"Location      : {CITY}, Kerala, India\n")
        f.write(f"Temperature   : {temp}°C\n")
        f.write(f"Condition     : {detailed_desc.capitalize()}\n")
        
        if is_hot or is_raining:
            f.write("Alert Status  : ⚠️ TRIGGERED (Sending Email Notification)\n")
            f.write("==================================================\n")
            send_email_alert(temp, detailed_desc, current_time, daily_quote)
        else:
            f.write("Alert Status  :  NORMAL (No Email Required)\n")
            f.write("==================================================\n")

def send_email_alert(temp, condition, run_time, quote):
    smtp_server = "smtp.gmail.com"
    port = 587
    email_password = os.getenv("EMAIL_PASSWORD") 
    
    if not email_password:
        print("❌ Email alert skipped: EMAIL_PASSWORD environment secret is missing.")
        return

    subject = f"⚠️ Weather Alert for {CITY}: Action Required!"
    body = (
        f"Hello Sathee,\n\n"
        f"Your automated bot detected critical weather shifts:\n"
        f"- Time: {run_time} (IST)\n"
        f"- Temp: {temp}°C\n"
        f"- Status: {condition.capitalize()}\n\n"
        f"Inspirational Quote of the Day:\n{quote}\n\n"
        f"Stay safe!"
    )
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(MY_EMAIL, email_password)
        server.sendmail(MY_EMAIL, MY_EMAIL, msg.as_string())
        server.quit()
        print("📨 Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    check_weather_and_alert()