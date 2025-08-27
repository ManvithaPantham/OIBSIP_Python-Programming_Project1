import speech_recognition as sr
import pyttsx3
import datetime
import requests
import wikipedia

 # Speak function
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)  # female voice
    engine.setProperty("rate", 170)  # speed
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # prevent hanging

#  Listen function
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
    except sr.UnknownValueError:
        return ""
    return query.lower()

#  Weather function
def get_weather(city):
    api_key = "e0fb714c9578fe4fb185d9e247cf3a20"  # 🔑 replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The weather in {city} is {temp}°C with {desc}."
        else:
            return f"Sorry, I couldn't find weather for {city}. Error: {data.get('message', '')}"
    except Exception as e:
        return f"Error while fetching weather: {str(e)}"

#  Main
def assistant():
    speak("Hello! I am your assistant. How can I help you?")
    while True:
        query = listen()

        if "time" in query:
            time = datetime.datetime.now().strftime("%H:%M")
            response = f"The time is {time}"
            print("Assistant:", response)
            speak(response)

        elif "date" in query:
            date = datetime.datetime.now().strftime("%d %B %Y")
            response = f"Today's date is {date}"
            print("Assistant:", response)
            speak(response)

        elif "weather" in query:
            speak("Please tell me the city name.")
            city = listen()
            if city:
                response = get_weather(city)
                print("Assistant:", response)
                speak(response)
            else:
                speak("Sorry, I didn't hear the city name.")

        elif "who is" in query:
            person = query.replace("who is", "").strip()
            try:
                info = wikipedia.summary(person, sentences=2)
                print("Assistant:", info)
                speak(info)
            except:
                response = f"Sorry, I could not find anything on {person}."
                print("Assistant:", response)
                speak(response)

        elif "stop" in query or "exit" in query:
            speak("Goodbye!")
            break

# Run
assistant()
