import speech_recognition as sr
import pyttsx3
import spacy
import openai_secret_manager
import openai
import random
import webbrowser
import os
import datetime

# Initialize the speech recognition engine
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the natural language processing library
nlp = spacy.load("en_core_web_sm")

# Set up the OpenAI API credentials
secrets = openai_secret_manager.get_secret("openai")
openai.api_key = secrets["api_key"]

# Define a function to capture audio input from the user's microphone and convert it into text
def get_audio():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand your command.")
            return ""
        except sr.RequestError:
            print("Sorry, I am not able to access the speech recognition service.")

# Define a function to generate audio output from text using the text-to-speech engine
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a function to extract the user's intent from their spoken command using natural language processing
def get_intent(command):
    doc = nlp(command)
    for token in doc:
        if token.dep_ == "ROOT":
            return token.lemma_
    return ""

# Start a conversation with the user
speak("Hi, how can I help you?")

# Define the wake word
wake_word = "hey chatbot"

# Start the listening loop
while True:
    # Listen for the wake word
    command = get_audio()
    if wake_word in command.lower():
        speak("How can I assist you?")
        break

# Start the command processing loop
while True:
    # Get the user's command as text input
    command = get_audio()
    
    # Extract the user's intent from the command
    intent = get_intent(command)
    
    # Process the user's command and provide a response
    if intent == "open":
        speak("Opening a web page.")
        webbrowser.open("https://www.google.com/")
    elif intent == "search":
        query = command.split("for")[-1]
        speak(f"Searching Google for {query}")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
    elif intent == "play":
        speak("Playing a random song.")
        songs_dir = "path/to/songs/directory"
        songs = os.listdir(songs_dir)
        random_song = random.choice(songs)
        os.startfile(os.path.join(songs_dir, random_song))
    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif intent == "joke":
        prompt = "Tell me a joke."
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5
        )
        speak(response.choices[0].text)
    elif intent == "goodbye":
        speak("Goodbye, have a nice day!")
        break
    else:
        speak("Sorry, I did not understand your command.")