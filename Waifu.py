import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import re
import threading
import time
import requests
import json


engine = pyttsx3.init()
newVoiceRate = 145
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', newVoiceRate)
name = "Alexa"
API_KEY = "tBSH-NxWvk48"
PROJECT_TOKEN = "t-TZUTkj4xff"
RUN_TOKEN = "tHbT-Tf3cnHT"


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(
            f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        data = json.loads(response.text)
        return data

    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Deaths:":
                return content['value']

        return "0"

    def get_country_data(self, country):
        data = self.data["country"]

        for content in data:
            if content['name'].lower() == country.lower():
                return content

        return "0"

    def get_list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())

        return countries

    def update_data(self):
        response = requests.post(
            f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language="es-MX")
        except Exception as e:
            speak("Me aburro, por favor dime algo..")

    return said.lower()


def main():
    print("Started Program")
    data = Data(API_KEY, PROJECT_TOKEN)
    END_PHRASE = "finalizar programa"
    country_list = data.get_list_of_countries()

    TOTAL_PATTERNS = {
        re.compile("[\w\s]+ total [\w\s]+ casos"): data.get_total_cases,
        re.compile("[\w\s]+ total casos"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ muertes"): data.get_total_deaths,
        re.compile("[\w\s]+ total muertes"): data.get_total_deaths
    }

    COUNTRY_PATTERNS = {
        re.compile("[\w\s]+ casos [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile("[\w\s]+ muertes [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
    }

    UPDATE_COMMAND = "actualizar"
    BUSCAR_COMMAND = "busca"

    while True:
        print("Listening...")
        text = get_audio()
        print(text)
        result = None

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break
        if text == UPDATE_COMMAND:
            result = "Los datos esta siendo actualizados, esto tomara un momento"
            data.update_data()
        if result:
            speak(result)

        if text.find(END_PHRASE) != -1:  # stop loop
            print("Exit")
            break
        if "reproduce" in text:
            music = text.replace('reproduce', ' ')
            pywhatkit.playonyt(music)
            speak(music)

        if "busca" in text:
            bus = text.replace('busca', ' ')
            pywhatkit.search(bus)
            speak('Buscando' + bus)

        if "hora" in text:
            hora = datetime.datetime.now().strftime('%I:%M %p')
            speak('Son las ' + hora)


main()
