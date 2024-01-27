import pyttsx3              #converte texto em fala
import speech_recognition as sr   #reconhecimento de fala do user
import keyboard
import os
import subprocess as sp

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

listening = False

def start_listening():
    global listening
    listening = True
    print("Link start")

def pause_listening():
    global listening
    listening = False
    print("Parando de ouvir")

keyboard.add_hotkey('ctrl+alt+s', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)

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
        if not 'pare' in query or 'sair' in query or 'fechar' in query:
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
        if listening:
            query = take_command().lower()
            if "como você está" in query:
                speak("Eu imagino que estou bem, senhor. E você, meu amigo ?")

            elif "Abra o prompt de comando" in query or "Abra o CMD" in query:
                speak("Abrindo o prompt de comando")
                os.system('start cmd')
            
            elif "Abra a câmera" in query:
                speak("Abrindo a câmera, senhor")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "Abra o bloco de notas" in query:
                speak("Abrindo o bloco de notas para você senhor")
                notepad_path = "C:\\Windows\\System32\\notepad.exe"
                os.startfile(notepad_path)

            elif "Abra o powershell" in query:
                speak("Abrindo o powershell para você senhor")
                powershell_path = "C:\\Users\\victt\\AppData\\Local\\Microsoft\\WindowsApps\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\wt.exe"
                os.startfile(powershell_path)

            elif "Abra o linux em terminal" in query:
                speak("Abrindo o ubuntu em terminal para o senhor")
                linux_path = "C:\\Users\\victt\\AppData\\Local\\Microsoft\\WindowsApps\\ubuntu.exe"
                os.startfile(linux_path)