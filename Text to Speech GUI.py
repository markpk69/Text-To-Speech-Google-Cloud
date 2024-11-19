import os
import time
from google.cloud import texttospeech
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Function to split text into chunks of up to `max_size` bytes
def split_text_to_bytes(text, max_size=5000):
    chunks = []
    current_chunk = ""

    for word in text.split():
        temp_chunk = current_chunk + " " + word
        if len(temp_chunk.encode("utf-8")) <= max_size:  # Check byte size
            current_chunk = temp_chunk
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Function to synthesize speech using Google Cloud Text-to-Speech
def text_to_speech_google(text, filename="output.mp3", language="en-US"):
    try:
        # Set up Google Cloud TTS client
        client = texttospeech.TextToSpeechClient()

        # Split the text into chunks
        text_chunks = split_text_to_bytes(text, max_size=5000)

        # Temporary files to store audio chunks
        temp_files = []

        for i, chunk in enumerate(text_chunks):
            print(f"Processing chunk {i+1}/{len(text_chunks)}...")
            synthesis_input = texttospeech.SynthesisInput(text=chunk)

            # Configure voice and audio settings
            voice = texttospeech.VoiceSelectionParams(
                language_code=language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # Send the synthesis request
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            # Save the response audio content to a temporary file
            temp_file = f"temp_chunk_{i}.mp3"
            with open(temp_file, "wb") as out:
                out.write(response.audio_content)
                temp_files.append(temp_file)

            # Wait for 2 seconds before processing the next chunk to avoid rate limits
            time.sleep(2)

        # Combine all temporary audio chunks into the final output file
        with open(filename, "wb") as output_file:
            for temp_file in temp_files:
                with open(temp_file, "rb") as temp_audio:
                    output_file.write(temp_audio.read())

        # Clean up temporary files
        for temp_file in temp_files:
            os.remove(temp_file)

        print(f"Audio file saved as {filename}")
        messagebox.showinfo("Success", f"Audio file saved as {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Tkinter GUI
def select_file():
    filepath = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
    )
    if filepath:
        with open(filepath, "r", encoding="utf-8") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, file.read())

def save_file_dialog():
    file_path = filedialog.asksaveasfilename(
        title="Save Audio File",
        defaultextension=".mp3",
        filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*")),
    )
    if file_path:
        output_filename.set(file_path)

def convert_to_audio():
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter or load text to convert.")
        return

    filename = output_filename.get()
    if not filename:
        messagebox.showwarning("Warning", "Please select a file to save the audio.")
        return

    language = language_code_var.get()
    text_to_speech_google(text, filename=filename, language=language)

# Main Tkinter GUI
root = tk.Tk()
root.title("Google Cloud Text-to-Speech")
root.geometry("600x500")

# Text area for input
text_area = tk.Text(root, wrap=tk.WORD, height=15, width=70)
text_area.pack(pady=10)

# Frame for options
options_frame = tk.Frame(root)
options_frame.pack(pady=5)

# Language selection dropdown
language_label = tk.Label(options_frame, text="Language Code:")
language_label.grid(row=0, column=0, padx=5, pady=5)

language_code_var = tk.StringVar(value="en-US")  # Default language
language_dropdown = ttk.Combobox(
    options_frame,
    textvariable=language_code_var,
    values=["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "zh-CN", "hi-IN", "ja-JP", "ar-XA", "ru-RU"],
    state="readonly",
    width=10,
)
language_dropdown.grid(row=0, column=1, padx=5, pady=5)

# Save file button
save_file_button = tk.Button(options_frame, text="Save Audio File As...", command=save_file_dialog)
save_file_button.grid(row=1, column=0, columnspan=2, pady=5)

# Output file path variable
output_filename = tk.StringVar()

# Buttons
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

load_button = tk.Button(buttons_frame, text="Load Text File", command=select_file)
load_button.grid(row=0, column=0, padx=10)

convert_button = tk.Button(buttons_frame, text="Convert to Audio", command=convert_to_audio)
convert_button.grid(row=0, column=1, padx=10)

# Run the main loop
root.mainloop()
