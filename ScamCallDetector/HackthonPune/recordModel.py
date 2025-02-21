from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__)

# Set the path to the ffmpeg executable
AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "C:\\ffmpeg\\bin\\ffprobe.exe"

# Load the model
model_path = "scam_detection_model.h5"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at {model_path}.")
model = tf.keras.models.load_model(model_path)

# Load the tokenizer
tokenizer_path = "tokenizer.pkl"
if not os.path.exists(tokenizer_path):
    raise FileNotFoundError(f"Tokenizer not found at {tokenizer_path}.")
with open(tokenizer_path, "rb") as f:
    tokenizer = pickle.load(f)

@app.route('/')
def home():
    return render_template('recordModal.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files['audio']

    try:
        # Read the uploaded audio file (WebM format)
        audio = AudioSegment.from_file(io.BytesIO(audio_file.read()), format="webm")

        # Export to WAV format
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        # Transcribe audio to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

    except Exception as e:
        return jsonify({"error": f"Error during transcription: {str(e)}"}), 500

    # Preprocess the text
    try:
        sequence = tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(sequence, maxlen=150, padding='post')
    except Exception as e:
        return jsonify({"error": f"Error during text preprocessing: {str(e)}"}), 500

    # Placeholder for audio features
    audio_features = np.random.rand(1, 40)

    # Make prediction
    try:
        prediction = model.predict([padded_sequence, audio_features])
        is_scam = prediction[0][0] > 0.5
    except Exception as e:
        return jsonify({"error": f"Error during prediction: {str(e)}"}), 500

    return jsonify({"text": text, "is_scam": bool(is_scam)})

if __name__ == '__main__':
    app.run(debug=True)