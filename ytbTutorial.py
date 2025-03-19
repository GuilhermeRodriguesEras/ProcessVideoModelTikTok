from vosk import Model, KaldiRecognizer
import pyaudio

model = Model("vosk-model-small-pt-0.3")
recognizer = KaldiRecognizer(model, 16000)