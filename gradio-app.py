# If you don't use pipenv, uncomment the following:
from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts

# AI Doctor System Prompt
system_prompt = """You have to act as a professional doctor, I know you are not, but this is for learning purposes. 
With what I see, I think you have .... 
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in your response. 
Your response should be in one long paragraph. Always answer as if you are talking to a real person. 
Do not respond as an AI model in markdown; your answer should mimic that of an actual doctor, not an AI bot. 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""

def process_inputs(audio_filepath, image_filepath):
    # Get API Key
    groq_api_key = os.getenv('GROQ_API_KEY')

    
    if not groq_api_key:
        return "Error: Missing GROQ API Key", "Error: Missing GROQ API Key", None

    # Speech to Text Conversion
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=groq_api_key, 
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # Analyze Image (If Provided)
    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + " " + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model="llama-3.2-11b-vision-preview"
        )
    else:
        doctor_response = "No image provided for me to analyze."
    print(f"Doctor response: {doctor_response}")

    # Convert Doctor's Response to Speech
    audio_output_path = "final.mp3"
    text_to_speech_with_gtts(input_text=doctor_response, output_filepath=audio_output_path)

    return speech_to_text_output, doctor_response, audio_output_path

# Create Gradio Interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("final.mp3")  # Fix: Match the generated file name
    ],
    title="AI Doctor with Vision and Voice"
)

# Run Gradio App
iface.launch(debug=True)
