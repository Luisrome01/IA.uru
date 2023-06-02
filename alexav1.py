import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
from datetime import datetime

#  variables
assitant_name = 'alexa'
keep_listening = True
wikipedia.set_lang('es')

# Name recognizer
recognizer = sr.Recognizer()

# Voice configuration
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150) # Velocidad de habla
engine.setProperty('volume', 1) #volumen 

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def get_user_command():
    # Activa microfono
    with sr.Microphone() as source:
        print('Escuchando...')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        command = "" # setea commando con valor vacio para evitar error al retornar
        
        try:
            command = recognizer.recognize_google(audio, language='es-MX').lower() #define el tipo de voz (esp mex)
        except:
            command = 'error'
            
    return command

def run_alexa(): #empezamos con los ciclos 
    command = get_user_command()
    
    if assitant_name in command:
        command = command.replace(assitant_name, '')
        command = command.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u") #reemplaza los acentos debido a erroes
        print(command)
        
        # Define topicos

        if 'estas ahi' in command:
            speak('Si, aqui estoy. Qué necesitas?')
            
        elif 'reproduce' in command:
            song = command.replace('reproduce', '')
            speak(f'Reproduciendo {song}')
            pywhatkit.playonyt(song)
            
        elif 'hora' in command:
            time = datetime.now().strftime('%I:%M %p')
            speak(f'La hora actual es {time}')
            
        elif 'busca' in command:                    #si escicah busca, avanza
            if 'wikipedia' in command:              #si escucah wikipedia, se desea buscar en wikipedia
                topic = command.replace('busca en wikipedia', '')    #biblioteca busca, summary recibe el tema, y el numero de oraciones (1), y auto_suggest=True para sugerencias si hay no exactas.
                info = wikipedia.summary(topic,1, auto_suggest = True)
                speak(info)
                
        elif 'cuanto es' in command:
            prompt = command.replace('cuanto es', '')       
            result = eval(prompt)
            speak(f'{prompt} is {result}')
        
        elif 'chiste' in command:
            joke = pyjokes.get_joke(language='es')
            speak(joke)

        elif 'gracias' in command:
            speak('no es nada') 
            
        elif 'detente' in command:
            speak('Ok, hasta luego.')
            return False
            
        elif 'error' in command:
            speak('Ocurrió un error escuchando tu comando. Intenta de nuevo')
        
    return True

while keep_listening:
    keep_listening = run_alexa()