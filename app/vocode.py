import speech_recognition as sr
import requests
from gtts import gTTS
from playsound import playsound
import os
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image
import subprocess


recognizer = sr.Recognizer()


last_created_file = None

def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=5)
        command = recognizer.recognize_google(audio, show_all=False)
        print(f"Command: {command}")
        return command.lower()

def speak_text(text):
    tts = gTTS(text=text, lang='en-gb')
    filename = "temp.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def create_new_python_file(directory, base_name="untitled"):
    """Create a new Python file with a default name in the specified directory."""
    global last_created_file
    file_path = os.path.join(directory, f"{base_name}.py")
    counter = 1
    
    while os.path.exists(file_path):
        file_path = os.path.join(directory, f"{base_name}_{counter}.py")
        counter += 1
    
    
    with open(file_path, 'w') as file:
        file.write("")
    
    print(f"Created new file: {file_path}")
    speak_text(f"Created a new file named {os.path.basename(file_path)}")
    last_created_file = file_path
    return file_path

def open_file_in_vscode(filepath):
    """Open the specified file in Visual Studio Code."""
    try:
        subprocess.run(["code", filepath], check=True)
        print(f"Opened {filepath} in VS Code.")
        speak_text(f"Opening {os.path.basename(filepath)} in VS Code, Boss.")
    except Exception as e:
        print(f"Failed to open {filepath} in VS Code: {e}")
        speak_text(f"Failed to open {os.path.basename(filepath)} in VS Code.")

def get_existing_code(filepath, max_lines=50):
    """Read and return the last 'max_lines' lines of code from the file."""
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
       
        relevant_code = ''.join(lines[-max_lines:])
        print(f"Relevant code in {filepath}:\n{relevant_code}")
        return relevant_code
    except Exception as e:
        print(f"Failed to read {filepath}: {e}")
        return ""

def update_code_in_file(new_code, filepath):
    try:
        with open(filepath, 'a') as file:
            file.write(new_code)
        print(f"Code appended to {filepath}")
        speak_text(f"Sure, updating the code in {os.path.basename(filepath)}, Boss.")
    except Exception as e:
        print(f"Failed to update {filepath} with the generated code: {e}")
        speak_text(f"Failed to update {os.path.basename(filepath)} with the generated code.")

def process_command(command, directory):
    speak_text("Sure Arjun, initiating process")
    
    global last_created_file
    if last_created_file and os.path.exists(last_created_file):
        
        existing_code = get_existing_code(last_created_file)
        prompt = f"{existing_code}\n\n# Continue the code with:\n{command}"
    else:
       
        last_created_file = create_new_python_file(directory)
        prompt = command

    try:
        response = requests.post(
            'http://localhost:8000/command',
            json={
                'prompt': prompt,
                'max_tokens': 15000
            },
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        response_data = response.json()
        new_code = extract_code(response_data['code'])

        
        open_file_in_vscode(last_created_file)
        update_code_in_file(new_code, last_created_file)

    except Exception as e:
        print(f"Error during command processing: {e}")
        speak_text("An error occurred while processing your command.")

def extract_code(response_text):
    """Extract and clean up the code from the response."""
    code_lines = []
    in_code_block = False
    for line in response_text.splitlines():
        if line.startswith("```"):
            in_code_block = not in_code_block
        elif in_code_block:
            
            if not line.strip().startswith("#"):
                code_lines.append(line)
    return "\n".join(code_lines)

def start_voice_assistant(icon, item):
    directory_to_watch = "~/Documents/"
    
    command = listen_command()

    if command:
        process_command(command, directory_to_watch)

def setup_tray_icon():
    
    icon_image_path = "./assets/vocode.png" 
    icon_image = Image.open(icon_image_path)
    
    
    icon = Icon("Voice Assistant", icon_image)
    
    
    menu = Menu(
        MenuItem('Activate Voice Assistant', start_voice_assistant),
        MenuItem('Quit', lambda icon, item: icon.stop())
    )


    icon.menu = menu

    icon.run()

if __name__ == "__main__":
    setup_tray_icon()
