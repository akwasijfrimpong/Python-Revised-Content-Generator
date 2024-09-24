import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def gemini_callout():

    apiKey = os.getenv('API_KEY')
    genai.configure(api_key=apiKey)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack.")
    print(response.text)

gemini_callout()

