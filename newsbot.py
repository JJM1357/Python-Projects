import requests

# Endpoints
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
NEWS_URL = "https://newsapi.org"  # Fixed: Points to News API endpoint
api_key = "0dee455253074f6781cd66b55c9ed296"

# Initialize fallback variables to prevent NameError if requests fail
temperature = "N/A"
wind_speed = "N/A"
time = "N/A"
articles_summary = "No headlines available today."

def format_headlines(articles_list):
    if not articles_list:
        return "No headlines found."
    
    formatted_str = ""
    for index, article in enumerate(articles_list, 1):
        title = article.get("title", "No Title")
        source = article.get("source", {}).get("name", "Unknown Source")
        formatted_str += f"{index}. {title} (Source: {source})\n\t"
    return formatted_str.strip()

def Send_Message(content):
    import smtplib
    from email.message import EmailMessage

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "jmjosephmartin82@gmail.com"
    SENDER_PASSWORD = "shnf tpaa etbf udyq"
    RECIPIENT_EMAIL = "josephmartyn9@gmail.com"

    msg = EmailMessage()
    msg["Subject"] = "Todays weather and news for you!!!"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(content)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()         
            server.starttls()     
            server.ehlo()         
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"There was an error sending the email: {e}")

# Weather parameters
weather_params = {
    "latitude": 9.71,
    "longitude": 76.68,
    "current": ["temperature_2m", "wind_speed_10m"],
    "timezone": "auto"
}

# News parameters
news_params = {
    "country": "in",
    "apiKey": api_key,
    "pageSize": 5
}

# Fetch Weather Data
try:
    response = requests.get(WEATHER_URL, params=weather_params, timeout=10)
    response.raise_for_status()
    weather_data = response.json()

    current = weather_data["current"]
    temperature = current["temperature_2m"]
    wind_speed = current["wind_speed_10m"]
    time = current["time"]
except Exception as err:
    print(f"Weather error occurred: {err}")

# Fetch News Data
try:
    # Fixed: Changed destination url to NEWS_URL
    response = requests.get(NEWS_URL, params=news_params, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    articles = data.get("articles", [])
    articles_summary = format_headlines(articles)  # Process list into string
    
except Exception as e:
    print(f"News error occurred: {e}")

# Construct and send the final email text
email_body = f"""
-------- Today's Weather ---------
\tTemperature 🌡️: {temperature} degrees C
\tWind Speed 💨: {wind_speed} km/h
\tTime: {time}
----------------------------------

---------- News Headlines ----------
\t{articles_summary}
----------------------------------
"""

Send_Message(email_body)
