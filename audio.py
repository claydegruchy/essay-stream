import os
from moviepy import AudioFileClip, AudioClip, concatenate_audioclips
from pydub import AudioSegment


def join(audio_folder, output_file="output.wav", silence_gap=0.750):

    audio_folder = "output/continuous/"

    audio_files = [audio_folder +
                   img for img in os.listdir(audio_folder) if img.endswith(".wav")]

    # 1000 for 1 sec, 2000 for 2 secs
    silence = AudioClip(lambda t: 0, duration=silence_gap, fps=44100)

    audios = []
    for audio in audio_files:
        audios.append(AudioFileClip(audio))
        audios.append(silence)

    audioClips = concatenate_audioclips([audio for audio in audios])
    audioClips.write_audiofile(output_file)
