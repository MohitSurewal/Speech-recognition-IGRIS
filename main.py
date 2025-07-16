
import speech_recognition as sr   #speech_recognition liabrary 
import webbrowser      #to access web_browser service 
import pyttsx3    #text_to_speech liabrary pyttsx3
import music_library   #inbuilt liabrary 
import pyjokes      #inbuilt jokes liabrary 



recognizer = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)    #female voice ( by using pyttsx3 )

                          
engine.setProperty('rate', 180)     # setting up new voice rate


def speak(text):
    
    engine.say(text)
    engine.runAndWait()
    
    
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        
    elif c.lower().startswith("play"):           #if user say anyword and if it startwith "play" and this will excute 
        song = c.lower().split(" ")[1]
        link = music_library.music[song]        #music_liabrary.py is a user defined liabrary for it 
        webbrowser.open(link)
    
    elif "joke" in c.lower():                   # this is tho tell the joke about programing
        joke = pyjokes.get_joke()
        print(f"Joke: {joke}")
        speak(joke)
        


if __name__ == "__main__":                 
    
    speak("Initializing Igris.....")
    while True:
    #it litsen wake word "Igris"
    #obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing....")
        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            word = r.recognize_google(audio)
            
            if(word.lower() == "arise"):     #wake word "Arise"
                speak("Igris Arise")
                #Listen for command
                with sr.Microphone() as source:
                    print("Igris Arise....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)         #use google recognizer 
                    
                    processCommand(command)
                    print(command)
                    speak(command)
                    
        except sr.UnknownValueError:
            print(" Could not understand audio.")            
                    
        except Exception as e:
            print(f"error {e}")
        

