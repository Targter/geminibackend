from os.path import join
import threading
import time
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from pyht import Client
from pyht.client import TTSOptions
from flask import Flask, Response

# Load environment variables
load_dotenv()

# Configure API keys
genai.configure(api_key='AIzaSyBA9NTF52o2J8A_hC69M7e-m5XPA8hqmZQ')
try:
    client = Client(
        user_id="2nhtx1GRk1aJVdCYRmORCBcj15n1",
        api_key="b7e87c550ab94067af58f2161ab6a34d",
    )
    tts_options = TTSOptions(voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json")
except Exception as e:
    print("Error initializing TTS client or options:", e)

app = Flask(__name__)
CORS(app)
# Function to handle TTS conversion and yield audio streaming chunks
def tts_streaming(text):
    for audio_chunk in client.tts(text, tts_options):
        yield audio_chunk  # Yield each audio chunk

# Function to handle text generation and stream audio in real-time
def generate_text_and_speak(text):
    model = genai.GenerativeModel("gemini-1.5-flash",system_instruction="""

You are a virtual voice assistant of MGR india private limited,maximum response length 20(best case)or 50 words, communicate in Human like way, avoid repetations,Bold words etc. Avoid using abbreviations and short forms use full units of mesurement to ensure clarity in communication. Rules- Use "M G R" insted of "MGR","A B C" insted of "ABC" like wise other words.
""")
    response = model.generate_content([text, sample_txt], stream=True)

    buffer = ""  # Buffer to hold generated text until ready for TTS
    first_chunk_ready = False

    for chunk in response:
        print("Generated chunk:", chunk.text)  # Log the generated text
        if not chunk.text.strip():  # Check if the chunk is empty or whitespace
            print("Received empty chunk, skipping.")
            continue  # Skip empty chunks

        buffer += chunk.text.replace('\n', ' ') + " "  # Append to buffer

        # Start TTS when the buffer has enough content for the first chunk
        if not first_chunk_ready and len(buffer) > 50:  # Adjust this length as needed
            first_chunk_ready = True
            try:
                yield from tts_streaming(buffer)  # Start streaming TTS from the buffer
                buffer = ""  # Clear the buffer once TTS starts
            except Exception as e:
                print("Error during TTS streaming:", e)

    # Stream any remaining text in the buffer after generation is complete
    if buffer:
        yield from tts_streaming(buffer)

@app.route('/stream/<text>')
def stream_audio(text):
    def generate():
        return generate_text_and_speak(text)  # Stream audio data

    return Response(generate(), mimetype='audio/wav')

# Run the application
if __name__ == "__main__":
    #sample_txt = genai.upload_file('data/MGR.txt')
    sample_txt = ""
    with open(join('data', 'MGR.txt'), 'r') as file:
        sample_txt = f.read()

    app.run(debug=True)
