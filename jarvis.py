import speech_recognition as sr
import pyttsx3
from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()
OPENAIKEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAIKEY)

r = sr.Recognizer()

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("Listening...")
                audio2 = r.listen(source2)
                print("Recognizing...")
                MyText = r.recognize_google(audio2)
                print(f"User : {MyText}")
                return MyText
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_chatGPT(messages):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)
    message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": message})
    return message

messages = []

while True:
    text = record_text()
    if text:
        messages.append({"role": "user", "content": text})
        response_content = send_to_chatGPT(messages)
        SpeakText(response_content)
        print("Jarvis : " + response_content)
