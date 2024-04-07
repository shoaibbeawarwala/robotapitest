from flask import Flask, render_template, request
import openai
import sounddevice as sd
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to call OpenAI API and get response
def call_openai_api(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ]
    )
    return response['choices'][0]['message']['content']


# Function to record audio from microphone
def record_audio():
    try:
        duration = 5  # Record for 5 seconds
        fs = 16000  # Sample rate
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        print("Recording audio...")
        sd.wait()  # Wait until recording is finished
        print("Recording completed.")
        return myrecording
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None


# Function to transcribe audio using rev.ai
def transcribe_audio(audio, rev_ai_api_key):
    # Implement rev.ai transcription logic here
    # For now, let's just return the audio as text
    return "".join([str(x) for x in audio])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Record audio from microphone
        audio = record_audio()
        if audio is None:
            return render_template('index.html',
                                   error="No microphone detected. Please connect a microphone and try again.")

        # Transcribe audio using rev.ai
        rev_ai_api_key = os.getenv("REV_AI_API_KEY")
        transcript = transcribe_audio(audio, rev_ai_api_key)

        # Generate response using OpenAI API
        response = call_openai_api(transcript)

        return render_template('index.html', response=response)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
