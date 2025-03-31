

# Load the .env file
# Step1: Setup GROQ API key
import os
import asyncio

GROQ_API_KEY = 'os.environ.get("GROQ_API_KEY")'

# Step2: Convert image to required format
import base64

image_path = "skin_rash.jpg"

def encode_image(image_path):   
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Step3: Setup Multimodal LLM 
from groq import Groq

query = "Is there something wrong with my face?"
model = "llama-3.2-90b-vision-preview"

def analyze_image_with_query(query, model, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)  
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion =client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content