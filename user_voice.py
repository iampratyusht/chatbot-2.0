import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    rec = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise..")
            rec.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            audio_data = rec.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved to {file_path}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

record_audio(file_path="voice_test.mp3")

import os
from groq import Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
stt_model = "whisper-large-v3"
audio_filepath = "voice_test.mp3"
audio_file = open(audio_filepath, "rb")
transcription = client.audio.transcriptions.create(
    model = stt_model,
    file = audio_file,
    language = "en"
)

print(transcription.text)

