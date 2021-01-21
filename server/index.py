from flask import Flask, request, jsonify, send_file, send_from_directory, abort
from gtts import gTTS
import os
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
import time
import atexit

audio_path = os.path.abspath('client/build/audio')
# audioPath = '/client/dist/audio'

app = Flask(__name__)


def removeAudios():
    for file_name in os.listdir(audio_path):
        file_path = os.path.join(audio_path, file_name)
        os.remove(file_path)

scheduler = BackgroundScheduler()
scheduler.add_job(func=removeAudios, trigger="interval", seconds=86400)
scheduler.start()

@app.route('/api/speak', methods=['POST'])
def sound_message():
    content = request.json    
    tts = gTTS(content['text'], lang=content['lang'])
    if not os.path.exists(audio_path):
        os.makedirs(audio_path)
    file_name = str(uuid.uuid4())
    full_file_name = audio_path + '/' + file_name + '.mp3'
    tts.save(full_file_name)
    if os.path.exists(full_file_name):
        return jsonify({'fileName': '/audio/' + file_name + '.mp3'})
    else:
        abort(404, description="Resource not found")

@app.route('/<path:path>')
def static_build(path):
    return send_from_directory("../client/build/", path)

@app.route('/audio/<path:path>')
def static_audio(path):
    return send_from_directory("../client/build/audio/", path)

@app.route('/static/css/<path:path>')
def static_style(path):
    return send_from_directory('../client/build/static/css/', path)

@app.route('/static/js/<path:path>')
def static_js(path):
    return send_from_directory('../client/build/static/js/', path)

@app.route("/")
def init():
    return send_from_directory("../client/build/", "index.html")

atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
