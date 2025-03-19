from vosk import Model, KaldiRecognizer
from preprocess import preprocessar_audio
import json
import wave

def transcrever_audio_vosk(arquivoEntrada, arquivo_txt):

    modelo_vosk = "vosk-model-small-pt-0.3"  
    model = Model(modelo_vosk) 

    preprocessar_audio(arquivoEntrada, "audios/audioModificado.mp3")

    with wave.open("audios/audioModificado.wav", "rb") as wf:
        recognizer_vosk = KaldiRecognizer(model, wf.getframerate())

        texto = ""
        while True:
            data = wf.readframes(20000)
            if len(data) == 0:
                break
            if recognizer_vosk.AcceptWaveform(data):
                resultado = json.loads(recognizer_vosk.Result())
                texto += resultado.get("text", "") + " "

        # Salvar a transcrição
        with open(arquivo_txt, "w", encoding="utf-8") as f:
            f.write(texto.strip())

        print("Transcrição salva em:", arquivo_txt)

transcrever_audio_vosk("audios/discurso.wav", "transcricao.txt")