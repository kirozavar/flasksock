from flask import Flask, render_template ,jsonify
from flask_sock import Sock
import speech_recognition as sr
import base64
import io

app = Flask(__name__)
sock = Sock(app)

transcriptions = ["test"]

@app.route('/test')
def test():
    return "test"

@app.route('/')
def index():
    return render_template('index.html', transcriptions=transcriptions)

@sock.route('/transcribe')
def transcribe_audio(ws):
    recognizer = sr.Recognizer()
    while True:
        audio_data = ws.receive()
        if audio_data is None:
            break

        audio_bytes = base64.b64decode(audio_data)
        audio_file = io.BytesIO(audio_bytes)

        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            transcriptions.append(text)
            ws.send(text)  
            print(text+"\n")
        except sr.UnknownValueError:
            ws.send("Could not understand audio")
        except sr.RequestError as e:
            ws.send(f"Speech Recognition service error: {e}")

@app.route('/get_transcriptions')
def get_transcriptions():
    return jsonify(transcriptions)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
