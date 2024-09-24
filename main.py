import google.generativeai as genai
import os
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys
import subprocess
from tempfile import gettempdir

from dotenv import load_dotenv
import requests

load_dotenv()


def text_to_speech_download(text): 
    session = Session(profile_name="akwasi")
    polly = session.client("polly")
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                        VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)
    if "AudioStream" in response:

        file = open('speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])


def gemini_callout():

    apiKey = os.getenv('API_KEY')
    genai.configure(api_key=apiKey)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack. less than 1500 char")
    print(response.text)
    text_to_speech = input("do you want text too speech?")
    if text_to_speech == "y":
        text_to_speech_download(response.text)
        
gemini_callout()




