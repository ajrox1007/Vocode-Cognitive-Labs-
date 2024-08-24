import speech_recognition as sr
import requests
from gtts import gTTS
from playsound import playsound
import os
import subprocess
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import shutil


recognizer = sr.Recognizer()

def speak_text(text):
    tts = gTTS(text=text, lang='en-gb')
    filename = "temp.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def listen_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for a command...")
        audio = recognizer.listen(source, timeout=5)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command: {command}")
            return command.lower()  
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
            speak_text("Sorry, I did not catch that.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            speak_text("Could not request results from Google Speech Recognition service.")
            return None

def extract_keywords(command):
    """Extract relevant keywords for searching from the voice command."""
    words_to_ignore = ['search', 'for', 'on', 'the', 'github', 'hugging', 'face', 'model', 'function', 'code']
    keywords = [word for word in command.split() if word not in words_to_ignore]
    return " ".join(keywords)

def search_github_repos(query, max_results=1, token=None):
    headers = {'Authorization': f'token {token}'} if token else {}
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repositories = response.json().get('items', [])[:max_results]
        return repositories
    else:
        print(f"Failed to fetch data from GitHub API: {response.status_code}")
        return []

def clone_repo(repo_url, clone_dir):
    try:
        if os.path.exists(clone_dir):
            shutil.rmtree(clone_dir)  
        subprocess.run(['git', 'clone', repo_url, clone_dir], check=True)
        print(f"Repository cloned to {clone_dir}")
        return True
    except Exception as e:
        print(f"Failed to clone repository: {e}")
        return False

def find_main_python_file(clone_dir):
    for root, dirs, files in os.walk(clone_dir):
        for file in files:
            if file.endswith('.py'):
                return os.path.join(root, file)
    return None

def open_file_in_vscode(filepath):
    """Open the specified file in Visual Studio Code."""
    try:
        subprocess.run(["code", filepath], check=True)
        print(f"Opened {filepath} in VS Code.")
        speak_text(f"Opening {os.path.basename(filepath)} in VS Code, Boss.")
    except Exception as e:
        print(f"Failed to open {filepath} in VS Code: {e}")
        speak_text(f"Failed to open {os.path.basename(filepath)} in VS Code.")

def search_github_and_generate_code(icon, item):
    speak_text("Sure Arjun, what function or feature should I look for on GitHub?")
    command = listen_command()
    if command:
        query = extract_keywords(command)
        repos = search_github_repos(query)
        if repos:
            first_repo = repos[0]
            repo_name = first_repo['full_name']
            repo_url = first_repo['clone_url']
            clone_dir = "/Users/arjunsethi/Documents/clone_dir"  
            if clone_repo(repo_url, clone_dir):
                main_python_file = find_main_python_file(clone_dir)
                if main_python_file:
                    open_file_in_vscode(main_python_file)
                else:
                    speak_text("No Python files found in the repository.")
            else:
                speak_text("Failed to clone the repository.")
        else:
            speak_text("No repositories found on GitHub.")

def start_voice_assistant(icon, item):
    directory_to_watch = "/Users/arjunsethi/Documents"  
    command = listen_command()
    if command:
        process_command(command, directory_to_watch)

def setup_tray_icon():
   
    icon_image_path = "/Users/arjunsethi/Documents/vocode.png"  
    icon_image = Image.open(icon_image_path)
    
   
    icon = Icon("Voice Assistant", icon_image)
    
    
    menu = Menu(
        MenuItem('Activate Voice Assistant', start_voice_assistant),
        MenuItem('Search GitHub for Code', search_github_and_generate_code),
        MenuItem('Quit', lambda icon, item: icon.stop())
    )
    
    
    icon.menu = menu
    
    
    icon.run()

if __name__ == "__main__":
    setup_tray_icon()
