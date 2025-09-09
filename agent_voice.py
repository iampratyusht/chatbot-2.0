import os
import elevenlabs
import subprocess
import platform
from gtts import gTTS
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


def tts_with_gtts(input_text, output_filepath="gtts_testing.wav"):
    language = "en"
    temp_mp3 = "temp.mp3"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(temp_mp3)


    sound = AudioSegment.from_mp3(temp_mp3)
    sound.export(output_filepath, format="wav")
    os.remove(temp_mp3)

    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Darwin":
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

input_text = "I am chatbot"
# tts_with_gtts(input_text=input_text, output_filepath = "gtts_testing.mp3")


def tts_with_elevenlabs(input_text, output_filepath="elevenlabs_testing.wav"):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )

    # Save ElevenLabs MP3
    temp_mp3 = "temp_elevenlabs.mp3"
    elevenlabs.save(audio, temp_mp3)

    # Convert MP3 → WAV
    sound = AudioSegment.from_mp3(temp_mp3)
    sound.export(output_filepath, format="wav")
    os.remove(temp_mp3)

    # Play audio
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Darwin":
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])  # or 'mpg123'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# input_text1 = "Hi, I am a chatbot project"
# tts_with_elevenlabs(input_text=input_text1, output_filepath="elevenlabs_testing.mp3")


# input_text = "Pehle to aap apana naam batayiye"
# tts_with_gtts(input_text=input_text, output_filepath = "gtts_autotesting.mp3")
# input_text1 = "baman baman"
# tts_with_elevenlabs(input_text=input_text1, output_filepath="elevenlabs_autotesting.mp3")
