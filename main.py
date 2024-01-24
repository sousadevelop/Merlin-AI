import pyttsx3              #converte texto em fala
import speech_recognition as sr   #reconhecimento de fala do user

from decouple import config
from datetime import datetime
from conv import random_text
from random import choice

engine = pyttsx3.init('sapi5')      #API da Microsoft usada para reconhecimento de fala
engine.setProperty('volume', 1.5)    #Define o volume da voz
engine.setProperty('rate', 255)     #Define a taxa de fala

voices = engine.getProperty('voices')       #Define a variável de voz
engine.setProperty('voices', voices[1].id)  #Escolhe a voz usada: 0 = homem | 1 = mulher

USER = config('USER')
HOSTNAME = config('BOT')

def speak(text):
    engine.say(text)
    engine.runAndWait()

#Função para a AI cumprimentar antes de responder
def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Bom dia {USER} !")
    elif (hour >= 12) and (hour < 18):
        speak(f"Boa tarte {USER} !")
    elif (hour >= 18) and (hour < 00):
        speak(f"Boa noite {USER} !")
    elif (hour >= 00) and (hour < 6):
        speak(f"Boa madrugada {USER} !")
    speak(f"Eu sou {HOSTNAME}. Como posso ajudá-lo ? {USER}")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        r.pause_threshold = 1       #tempo de pausa para espera da fala
        audio = r.listen(source)

    try:
        print("Reconhecendo...")
        query = r.recognize_google(audio, language='pt-br')
        print(query)
        if not 'pare' in query or 'sair' or 'fechar' in query:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Boa noite senhor, até logo!")
            else:
                speak("Tenha um bom dia senhor")
            exit()
    
    except Exception:
        speak("Desculpe-me, eu não consegui lhe entender. Você poderia repetir, por favor ?")
        query = 'None'
    return query

if __name__ == '__main__':
    greet_me()
    while True:
        query = take_command().lower()
        if "como você está" in query:
            speak("Eu imagino que estou bem, senhor. E você, meu amigo ?")