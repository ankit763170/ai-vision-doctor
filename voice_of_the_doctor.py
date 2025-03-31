import os
import subprocess
import platform
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"

    # Generate Speech
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    # Detect OS and play audio
    os_name = platform.system()
    
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['start', output_filepath], shell=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['mpg123', output_filepath])  # Use mpg123 for mp3 files
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Example Usage
# input_text = "Hi, this is AI with Ankit, and it's the AI voice of Ankit!"
# text_to_speech_with_gtts(input_text, "gtts_testing_autoplay.mp3")
