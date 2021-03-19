import speech_recognition as sr
import pyttsx3
import time
listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
name = "Alexa"
for voice in voices:
    print(voice)

def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
       with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice , language= "es-MX")
            if name in rec:
                print(rec)
            return rec

    except:
       pass
    

def run():
    rec = listen()

    if "Reproduce" in rec:
        talk("rec")
        
run()