from vosk import Model, KaldiRecognizer
from preprocess import preprocessar_audio
import json
import wave

def segundos_para_tempo(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int(segundos % 60)
    milissegundos = int((segundos - int(segundos)) * 1000)
    return f"{horas:02}:{minutos:02}:{segundos:02},{milissegundos:03}"

def transcrever_audio_vosk(arquivoEntrada, arquivo_srt):
    modelo_vosk = "vosk-model-small-pt-0.3"
    model = Model(modelo_vosk)

    preprocessar_audio(arquivoEntrada, "audios/audioModificado.wav")

    with wave.open("audios/audioModificado.wav", "rb") as wf:
        recognizer_vosk = KaldiRecognizer(model, wf.getframerate())
        recognizer_vosk.SetWords(True) 
        
        legendas = []
        index = 1
        tempo_inicio = None
        texto_legenda = ""

        while True:
            data = wf.readframes(20000)
            if len(data) == 0:
                break
            if recognizer_vosk.AcceptWaveform(data):
                resultado = json.loads(recognizer_vosk.Result())

                if "result" in resultado:
                    for palavra in resultado["result"]:
                        if tempo_inicio is None:
                            tempo_inicio = palavra["start"]
                        texto_legenda += palavra["word"] + " "

                        if palavra["end"] - tempo_inicio >= 5.0 or palavra["word"].endswith(('.', '!', '?')):
                            tempo_fim = palavra["end"]
                            legendas.append((index, tempo_inicio, tempo_fim, texto_legenda.strip()))
                            index += 1
                            tempo_inicio = None
                            texto_legenda = ""

        # Criar e salvar o arquivo SRT
        with open(arquivo_srt, "w", encoding="utf-8") as f:
            for idx, start, end, text in legendas:
                f.write(f"{idx}\n")
                f.write(f"{segundos_para_tempo(start)} --> {segundos_para_tempo(end)}\n")
                f.write(f"{text}\n\n")

        print("Legendas salvas em:", arquivo_srt)


transcrever_audio_vosk("audios/discurso.wav", "legendas.srt")