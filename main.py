import speech_recognition as sr   
import webbrowser                 
import pyttsx3                   
import music_library             
import pyjokes                    
import requests                   


OPENWEATHER_API_KEY = "c2e46c0649f7a423c313ade86d820588"   


recognizer = sr.Recognizer()
engine = pyttsx3.init()


voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice
engine.setProperty('rate', 180)  # speaking speed


def speak(text):
    print("IGRIS:", text)
    engine.say(text)
    engine.runAndWait()


def get_weather(city_name=""):
    
    if not OPENWEATHER_API_KEY:
        return "Weather API key is not configured properly."
    if not city_name:
        return "Please specify a city name."

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={OPENWEATHER_API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return f"Couldn't fetch weather for {city_name}."
        data = r.json()

        main = data.get("weather", [{}])[0].get("description", "no description")
        temp = data.get("main", {}).get("temp")
        feels_like = data.get("main", {}).get("feels_like")
        humidity = data.get("main", {}).get("humidity")

        summary = (
            f"The weather in {city_name} is {main}. "
            f"Temperature is {temp}°C, feels like {feels_like}°C, with {humidity}% humidity."
        )
        return summary

    except Exception as e:
        return f"Error fetching weather: {e}"


last_city = None  # stores the last used city

def processCommand(command):

    global last_city
    command = command.lower()
    print("Processing command:", command)

    
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

   
    elif command.startswith("play"):
        parts = command.split(" ", 1)
        if len(parts) > 1:
            song = parts[1].strip()
            link = music_library.music.get(song)
            if link:
                speak(f"Playing {song} from your library.")
                webbrowser.open(link)
            else:
                speak(f"Sorry, I couldn't find {song} in your music library.")
        else:
            speak("Please say the song name after play.")


    elif "joke" in command:
        joke = pyjokes.get_joke()
        print("Joke:", joke)
        speak(joke)

    
    elif "weather" in command:
        words = command.split()
        city = ""

        
        if "in" in words:
            city = " ".join(words[words.index("in") + 1:])
            last_city = city  

       
        if not city:
            if last_city:
                speak(f"Fetching weather for your last city, {last_city}.")
                report = get_weather(last_city)
                speak(report)
                return
            else:
                speak("Please tell me the city name.")
                print("Listening for city name...")
                try:
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        city = recognizer.recognize_google(audio)
                        last_city = city
                        print(f"City recognized: {city}")
                except sr.WaitTimeoutError:
                    speak("You didn’t say anything. Please try again.")
                    return
                except sr.UnknownValueError:
                    speak("Sorry, I could not understand the city name.")
                    return
                except Exception as e:
                    print("Error recognizing city:", e)
                    speak("Sorry, I could not get the city name.")
                    return

        speak(f"Fetching weather report for {city}.")
        report = get_weather(city)
        speak(report)

    
    else:
        speak("Sorry, I didn’t understand that command.")


if __name__ == "__main__":
    speak("Initializing Igris.....")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("\nListening for wake word......")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if word.lower() == "arise":  # wake word
                speak("Igris Arise")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Listening for your command...")
                    audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)

        except sr.WaitTimeoutError:
            print("Listening timed out. Waiting again...")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except Exception as e:
            print("Error:", e)
