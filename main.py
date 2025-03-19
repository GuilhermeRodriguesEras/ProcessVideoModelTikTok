
from moviepy import VideoFileClip

# Create the audio file
input_file = "videos/discurso.mp4"
output_file = "discurso.wav"

video = VideoFileClip(input_file)
video.audio.write_audiofile(output_file)