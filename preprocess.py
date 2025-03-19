from pydub import AudioSegment
import noisereduce as nr
import numpy as np

def preprocessar_audio(arquivo_entrada, arquivo_saida, sample_rate=16000):
    # Carregar o arquivo de áudio
    audio = AudioSegment.from_wav(arquivo_entrada)

    # Converter para mono
    audio = audio.set_channels(1)

    # Alterar a taxa de amostragem
    audio = audio.set_frame_rate(sample_rate)

    # Exportar o novo arquivo
    audio.export(arquivo_saida, format="wav")


def reduzirRuido(arquivo_entrada):
    audio = AudioSegment.from_wav(arquivo_entrada)

    samples = np.array(audio.get_array_of_samples())

    reduced_noise = nr.reduce_noise(y=samples, sr=audio.frame_rate)

    reduced_audio = AudioSegment(
        reduced_noise.tobytes(), 
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    reduced_audio += 50

    reduced_audio.export(arquivo_entrada, format="wav")
