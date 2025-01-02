import customtkinter as ctk
import tkinter as tk
import pygame
import tempfile
import requests
import openai

# Initialize pygame mixer
pygame.mixer.init()

# Set up API keys
openai.api_key = "{Insert OpenAI API key here}"
elevenlabs_api_key = "{Insert ElevenLabs API key here}"
voice_id = "{Insert desired ElevenLabs Voice ID here}"

# Set dark mode and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Function to get GPT-4 response
def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response['choices'][0]['message']['content']

# Function to convert text to speech using ElevenLabs API
def text_to_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        'xi-api-key': elevenlabs_api_key,
        'Content-Type': 'application/json'
    }
    
    data = {'text': text,
            'stability': 30
            }
    
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        audio_content = response.content
        play_audio(audio_content)
    else:
        print("Error:", response.text)

# Function to play audio using pygame
def play_audio(audio_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file.write(audio_content)
        temp_audio_file.flush()
        temp_audio_path = temp_audio_file.name

    pygame.mixer.music.load(temp_audio_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

# Function to send a message
def send_message():
    user_message = entry.get()
    chat_history.insert(tk.END, f"You: {user_message}\n", 'user')  # Insert with tag
    entry.delete(0, tk.END)
    
    messages.append({"role": "user", "content": user_message})
    
    bot_response = get_chatgpt_response(messages)
    
    chat_history.insert(tk.END, f"Evil Scott: {bot_response}\n", 'bot')  # Insert with tag
    chat_history.yview(tk.END)
    
    messages.append({"role": "assistant", "content": bot_response})
    
    app.after(100, lambda: text_to_speech(bot_response))

# Set up the main window
app = ctk.CTk()

app.title("Luna Chat")
app.geometry("1000x1000")
app.configure(fg_color="#1a1a1a")  # Dark background

# Chat history display
chat_history = tk.Text(app, wrap=tk.WORD, bg="#1a1a1a", fg="#c2c2c2", font=("Arial", 16), insertbackground="#ffffff")
chat_history.tag_config('user', foreground='#c4a000')  # Gold for user messages
chat_history.tag_config('bot', foreground='#FF0000')  # Red for bot messages
chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# User input entry
entry = ctk.CTkEntry(app, placeholder_text="Type your message...", font=("Arial", 16), text_color="#ffffff")
entry.pack(pady=10, padx=10, fill=tk.X, side=tk.LEFT, expand=True)

# Send button
send_button = ctk.CTkButton(app, text="Send", command=send_message, fg_color="#5a5a5a", hover_color="#3a3a3a", text_color="#ffffff")
send_button.pack(pady=10, padx=10, side=tk.RIGHT)

# Read background file:
file = open("bot_background_master.txt", "r")
bot_background = file.read()
file.close()

# Conversation history
messages = [{"role": "system", "content": bot_background}]

# Launch app
app.mainloop()