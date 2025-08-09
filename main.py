import speech_recognition as sr
import pyttsx3

from agent import agent_executor

# Initialize Text-to-Speech Engine


def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    print(f"AGENT: {text}")
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def get_keyboard_input():
    """Gets user input from the keyboard."""
    print("\n------------------------------------")
    # We use the built-in input() function to get typed text
    user_input = input("👨 TYPE YOUR COMMAND: ")
    return user_input
# Initialize Speech Recognition
# r = sr.Recognizer()

# def listen():
#     """Listens for voice input from the microphone and converts it to text."""
#     with sr.Microphone() as source:
#         print("\nListening...")
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source)
    
#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"USER: {query}")
#         return query
#     except Exception as e:
#         speak("Sorry, I did not understand that. Please try again.")
#         return "None"
    
if __name__ == "__main__":
    speak("Hello! I am your Smart Study Buddy. How can I help you today?")

    while True:

        user_input = get_keyboard_input()

        if user_input.lower() in ["none", ""]:
            continue

        if user_input.lower() in ["goodbye", "exit", "quit"]:
            speak("Goodbye! Happy studying!")
            break

        response = agent_executor.invoke({"input": user_input})

        speak(response['output'])