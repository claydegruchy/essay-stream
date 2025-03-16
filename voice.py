from TTS.api import TTS
import torch
import argparse
import sys
import os

params = {
    "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
    "speaker_wav": "samples/DerekJacobi.wav",
    "language_idx": "en",
}


def init_tts():

    print("Get device")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Init TTS")
    tts = TTS(params["model_name"]).to(device)


def tts(text, output="out.wav", emotion="neutral"):
    print("tts...", text, output)

    params = {
        **params,
        "text": text,
        "out_path": output,
        "emotion": emotion
    }

    # List available 🐸TTS models
    # print(TTS().list_models())

    print("Run TTS")
    # Text to speech list of amplitude values as output
    # wav = tts.tts(
    # text=text,
    #   speaker_wav=params["speaker_wav"],
    #               language=params["language_idx"],
    #               file_path="out.wav"
    #               )
    # Text to speech to a file
    tts.tts_to_file(
        text=text,
        speaker_wav=params["speaker_wav"],
        language=params["language_idx"],
        file_path=params["out_path"],
        emotion=params["emotion"]
    )


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def parse(text):
    from nltk.tokenize import sent_tokenize, word_tokenize
    import nltk

    nltk.download('punkt_tab')

    return sent_tokenize(text)


def main():

    init_tts()
    eg = 'its me, derek jacobi!'
    i = 0
    for text in parse(eg):
        i += 1
        tts(text=text,
            output="out/{i}.wav".format(i=i))

    return
    parser = argparse.ArgumentParser(description="CLI Tool")
    parser.add_argument("input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-u", "--uppercase", action="store_true",
                        help="Convert text to uppercase")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    content = read_file(args.input)

    if args.output:
        write_file(args.output, content)
        return

    parse(content)


if __name__ == "__main__":
    main()
