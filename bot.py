import requests
from datetime import datetime

def get_weather():
    try:
        response = requests.get("https://wttr.in/?format=3")
        if response.status_code == 200:
            return response.text.strip()
        return "Weather unavailable today."
    except Exception:
        return "Could not connect to weather service."

def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()
            return f'"{data[0]["q"]}" — {data[0]["a"]}'
        return "Stay positive and keep coding!"
    except Exception:
        return "Keep moving forward!"

def main():
    weather = get_weather()
    quote = get_quote()
    
    # Get current date and time formatted nicely
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create the text summary layout
    summary = f"""=====================================
PULSE DAILY SUMMARY
Generated on: {current_time}
=====================================

🌤️ CURRENT WEATHER:
{weather}

💭 DAILY INSPIRATION:
{quote}

=====================================\n"""
    
    # Save it locally to a file named 'daily_summary.txt'
    with open("daily_summary.txt", "w", encoding="utf-8") as file:
        file.write(summary)
    
    print("Success! daily_summary.txt has been generated.")

if __name__ == "__main__":
    main()
    