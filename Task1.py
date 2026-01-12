import speech_recognition as sr
import pyttsx3
import datetime
import time
import requests

# ---------- CONFIG ----------
WEATHER_API_KEY = "11c5ae9c10bfdc9b1fb41d9380bbf25b"
NEWS_API_KEY = "6f912309491b4ffbae9ddfc6077d6a87"
CITY = "Mumbai"
WAKE_WORD = "hey assistant"
# ----------------------------

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
            command = r.recognize_google(audio)
            print("You:", command)
            return command.lower()
        except:
            return ""

# -------- FEATURES --------

def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            speak(f"It is {temp} degrees Celsius with {desc} in {CITY}")
        else:
            speak("Weather data not available")
    except:
        speak("Weather service error")

def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        data = requests.get(url).json()
        speak("Here are the top news headlines")
        for article in data["articles"][:5]:
            speak(article["title"])
    except:
        speak("News service error")

def set_reminder():
    speak("What should I remind you about?")
    reminder = listen()
    if not reminder:
        speak("Reminder cancelled")
        return

    speak("In how many seconds?")
    seconds = listen()
    if seconds.isdigit():
        speak("Reminder set")
        time.sleep(int(seconds))
        speak("Reminder alert")
        speak(reminder)
    else:
        speak("Invalid time")

# -------- MAIN --------

def assistant():
    speak("Assistant is running")

    while True:
        command = listen()
        if not command:
            continue

        # Remove wake word if present
        if WAKE_WORD in command:
            command = command.replace(WAKE_WORD, "").strip()

        print("Processed Command:", command)

        if "time" in command:
            get_time()
        elif "weather" in command:
            get_weather()
        elif "news" in command:
            get_news()
        elif "reminder" in command:
            set_reminder()
        elif "exit" in command or "stop" in command:
            speak("Goodbye")
            break
        else:
            speak("Please say time, weather, news, or reminder")

# -------- RUN --------
assistant()
