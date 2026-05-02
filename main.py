import time
import tkinter as tk
from tkinter import scrolledtext
import webbrowser
import speech_recognition as sr
import pyttsx3
import pyjokes
import requests
import music_library
import Igris_Api
import random
import os
import pywhatkit

OPENWEATHER_API_KEY = "c2e46c0649f7a423c313ade86d820588"

recognizer = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty("voices")
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)   # female voice, [0] is usually male
engine.setProperty("rate", 160)



def speak(text):
    log(f"IGRIS: {text}")
    engine.say(text)
    engine.runAndWait()
    


def log(message):
    timestamp = time.strftime("%H:%M:%S")
    log_area.insert(tk.END, f"[{timestamp}] {message}\n")
    log_area.see(tk.END)
    app.update()
    
# mausam report function

def get_weather(city):
    if not OPENWEATHER_API_KEY:
        return "Weather API key is missing."

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&units=metric&appid={OPENWEATHER_API_KEY}"
    )

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return f"Could not fetch weather for {city}."

        data = r.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        return (
            f"The weather in {city} is {desc}. "
            f"Temperature is {temp} degree Celsius "
            f"with humidity {humidity} percent."
        )

    except Exception as e:
        return f"Weather error: {e}"

# number guessing game

def play_number_game():
    number = random.randint(1, 50)
    guesses = 0

    speak("Opening number guessing game")
    speak("I have selected a number between 1 and 50")

    while True:
        try:
            speak("Say your guess")

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=2)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)

            user_input = recognizer.recognize_google(audio)
            

            guess = int(user_input)
            guesses += 1

            if guess > number:
                speak(f"Lower number please. and your number {guess} attempts are {guesses}")
            elif guess < number:
                speak(f"Higher number please. and your number {guess} attempts are {guesses}")
                
                
            elif guess == "exit":
                speak("Exiting the game.")
                break
            else:
                speak(f"Congratulations! You guessed number {number} in {guesses} attempts")
                break
            
            

        except sr.UnknownValueError:
            speak("I did not understand. Try again.")
        except ValueError:
            speak("Please say a number")
        except Exception as e:
            speak("Something went wrong.", e)
            break

# commmands start fromm here:

def process_command(command):
    command = command.lower()
    log(f"Processing command: {command}")

   
    if "news" in command or "headlines" in command:
        speak("Fetching top three headlines.")
        headlines = Igris_Api.get_news()
        for i, h in enumerate(headlines, 1):
            speak(f"Headline {i}: {h}")
        return


    
    if "time" in command or "date" in command or "samay" in command:
        now = time.localtime()
        current_time = time.strftime("%I:%M %p", now)
        current_date = time.strftime("%B %d, %Y", now)
        speak(f"The current time is {current_time} and today's date is {current_date}.")
        log(f"Time: {current_time}, Date: {current_date}")
        return 

   
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        
    

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
        
        
    elif "open qr code generator" in command or "code generator" in command:
        speak("opening QR code Generator")
        webbrowser.open("https://qr-code-generator-smks.onrender.com/")

    
    elif "version" in command:
        speak("My version is one point O. I was created in Surewal.tech.")

    elif "who created you" in command:
        speak("I was created in Surewal.tech which is owned by Mohit Surewal.")
        
        
        
        
    elif "shutdown" in command or "turn off laptop" in command or "band karo laptop" in command:
        log("Processing shutdown command.")
        speak("Are you sure you want to shut down your system?")

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=2)
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)

            confirmation = recognizer.recognize_google(audio).lower()
            log(f"Confirmation heard: {confirmation}")

            if "kar do" in confirmation or "confirm" in confirmation or "kardo" in confirmation:
                log("Shutting down system...")
                speak("Shutting down your system, Master!")
                os.system("shutdown /s /t 10")

            elif "no" in confirmation or "cancel" in confirmation:
                speak("Shutdown cancelled.")

            else:
                log("I did not understand. Shutdown cancelled for safety.")

        except sr.UnknownValueError:
            speak("Sorry, I could not understand you. Shutdown cancelled.")

        except sr.WaitTimeoutError:
            speak("No response received. Shutdown cancelled.")

        except Exception as e:
            log(f"Error: {e}")
            speak("Something went wrong. Shutdown cancelled.")
            
            
    if "restart" in command or "restart laptop" in command:
        log("Processing restart command.")
        speak("Are you sure you want to restart your system?")

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=2)
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)

            confirmation = recognizer.recognize_google(audio).lower()
            log(f"Confirmation heard: {confirmation}")

            if "yes" in confirmation or "confirm" in confirmation:
                log("Restarting system...")
                speak("Restarting your system, Master!")
                os.system("shutdown /r /t 10")

            elif "no" in confirmation or "cancel" in confirmation:
                speak("restart cancelled.")

            else:
                speak("I did not understand. restart cancelled for safety.")

        except sr.UnknownValueError:
            speak("Sorry, I could not understand you. restart cancelled.")

        except sr.WaitTimeoutError:
            speak("No response received. restart cancelled.")

        except Exception as e:
            log(f"Error: {e}")
            speak("Something went wrong. restart cancelled.")
                
                

        

    elif command.startswith("play") :
        parts = command.split(" ", 1)
        if len(parts) > 1:
            song = parts[1].strip()
            link = music_library.music.get(song)
            if link:
                speak(f"Playing {song} from your library.")
                webbrowser.open(link)
            else:
                 song not in music_library.music
            speak(f"playing {song} on youtube")
            pywhatkit.playonyt(song)
        else:
            speak("Please specify a song to play.")     
    
    
    
    
    
    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)
        
    elif "exit" in command or "so jao" in command or "" :
        speak("ok sorcerer, going to sleep....")
        app.quit()

    elif "game" in command or "start game" in command:
        play_number_game()
        
    
    elif "weather" in command or "mausam " in command:
        speak("Please tell me the city name.")

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            city = recognizer.recognize_google(audio)
            log(f"City heard: {city}")

            speak(f"Fetching weather for {city}")
            report = get_weather(city)
            speak(report)

        except sr.UnknownValueError:
            speak("Sorry, I could not understand the city name.")

        except sr.WaitTimeoutError:
            speak("You did not say the city name.")

        except Exception as e:
            log(f"Error: {e}")
            speak("Something went wrong while fetching weather.")


# litsen Function

def start_listening():
    
    speak("Listening started.")
    

    while True:
        
        
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                log("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            word = recognizer.recognize_google(audio)
            log(f"Heard: {word}")

            if word.lower() == "arise" or word.lower() == "let's get to work" or word.lower() == "jago":
                speak("Igris Arise")
                
            
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    log("Listening for command...")
                    audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)

                command = recognizer.recognize_google(audio)
                log(f"Command: {command}")
                process_command(command)
                
            elif word.lower() =="exit" or word.lower() == "sleep" or word.lower() == "so jao" or word.lower() == "band karo" or word.lower() == "band kar do":
                speak("going sorcerer....")
                break
            
            

        except sr.UnknownValueError:
            log("Could not understand audio.")
        except sr.WaitTimeoutError:
            log("Listening timed out.")
        except Exception as e:
            log(f"Error: {e}")


# tikinter GUI setup

app = tk.Tk()
app.title("SPEECH - RECOGNITION (IGRIS) V1.O")
app.geometry("900x550")
app.configure(bg="#0b0f1a")

top = tk.Frame(app, bg="#0b1220")
top.pack(fill="x", padx=10, pady=10)

start_btn = tk.Button(
    top, text="Start Listening",
    command=start_listening,
    bg="#f01505", fg="white",
    width=18
)
start_btn.pack(side="left", padx=8)

tk.Label(
    top, text="Manual Command:",
    bg="#0b1220", fg="white"
).pack(side="left", padx=8)

manual_entry = tk.Entry(top, width=40)
manual_entry.pack(side="left", padx=8)


def manual_send():
    cmd = manual_entry.get().strip()
    if cmd:
        log(f"Manual command: {cmd}")
        process_command(cmd)
        manual_entry.delete(0, tk.END)


tk.Button(
    top, text="Send",
    command=manual_send,
    bg="#2ecc71", fg="white",
    width=10
).pack(side="left", padx=8)

log_area = scrolledtext.ScrolledText(
    app, wrap=tk.WORD,
    bg="#08121a", fg="#e6f0ff",
    font=("Times New Roman", 14)
)
log_area.pack(fill="both", expand=True, padx=10, pady=10)




log("IGRIS GUI started.")
speak("Hi, I am Igris. Version one point o.")

app.mainloop()
