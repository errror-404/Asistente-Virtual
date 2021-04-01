import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit



listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice',voices[2].id)
name = "Alexa"


def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
       with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice , language= "es-MX")
            if name in rec:
                rec = rec.replace(name , "")
                print(rec)
            

    except:
       pass
    return rec

def run():
    rec = listen()

    if "Reproduce" in rec:
        music = rec.replace('Reproduce', ' ')
        pywhatkit.playonyt(music)
        talk('reproduciendo' + music)
       
   
    if "Busca" in rec:
        bus = rec.replace('Busca', ' ')
        pywhatkit.search(bus)
        talk('Buscando' + bus)
   
    if "hora" in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk('Son las ' + hora)
   
        
run()