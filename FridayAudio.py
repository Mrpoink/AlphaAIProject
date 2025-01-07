import pyaudio
import wave
import simpleaudio as sa
import speech_recognition as sr

cred = open("client_secret.json", "r")

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()

def get_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    default_info = p.get_device_info_by_index(0)
    default_info_2 = p.get_device_info_by_index(2)
    default_info_1 = p.get_device_info_by_index(1)

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    print(default_info)
    print(default_info_2)
    print(default_info_1)
    for i in range(p.get_host_api_count()):
        info = p.get_host_api_info_by_index(i)
        print(i)
        if info['name'] == 'WASAPI':
            wasapi_index = i
            print(wasapi_index)
            break



def record():
    stream = audio.open(
        format=FORMAT,
        channels=1,
        rate=RATE,
        input=True,
        output=False,
        frames_per_buffer=CHUNK,
        input_device_index=1,
    )
    print("recording")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def play():
    wave_obj = sa.WaveObject.from_wave_file(WAVE_OUTPUT_FILENAME)
    play_obj = wave_obj.play()

    play_obj.wait_done()

def transcribe():
    r = sr.Recognizer()
    m = sr.Microphone()

    with m as source:
        r.adjust_for_ambient_noise(source)

    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio_data = r.record(source)

    try:
        text = r.recognize_google_cloud(audio_data, credentials_json="gen-lang-client.json")
        print(text)

        if text.contains("period"):
            return text
        if text.contains("Hey, Friday"):
            with sr.Microphone() as source:
                audio = r.listen(source)

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud")

transcribe()

