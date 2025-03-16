
# import argparse
# import sys
# import os
print("Imports done")

base_params = {
    "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
    "speaker_wav": "samples/storyoffilm.wav",
    "language_idx": "en",
}


tts = None


def init_tts():
    print("Starting imports")
    from TTS.api import TTS
    import torch
    print("Get device")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Init TTS")
    return TTS(base_params["model_name"]).to(device)


def run_tts(tts, text, output="out.wav", emotion="neutral"):
    print("tts...", text, output)

    params = {
        **base_params,
        "text": text,
        "out_path": output,
        "emotion": emotion
    }

    # List available 🐸TTS models
    # print(TTS().list_models())

    print("Run TTS")
    # Text to speech to a file
    tts.tts_to_file(
        text=text,
        speaker_wav=params["speaker_wav"],
        language=params["language_idx"],
        file_path=params["out_path"],
        emotion=params["emotion"]
    )


def parse(text):
    from nltk.tokenize import sent_tokenize, word_tokenize
    import nltk

    nltk.download('punkt_tab')

    return sent_tokenize(text)


base_template = """Question: {question}

    Answer: """


def local_llm(question, template=base_template):
    from langchain.llms.huggingface_pipeline import HuggingFacePipeline
    hf = HuggingFacePipeline.from_model_id(
        model_id="microsoft/DialoGPT-medium", task="text-generation", pipeline_kwargs={"max_new_tokens": 200, "pad_token_id": 50256},
    )
    from langchain.prompts import PromptTemplate
    prompt = PromptTemplate.from_template(template)
    chain = prompt | hf

    return chain.invoke({"question": question})


def get_coordinates(doc_dir):
    return


def read_document(doc_dir):
    # we read the doc into blocks
    # then we use some coordinates to ensure we only get the blocks within an area
    # that we actually want
    import pymupdf

    doc = ""

    # out = open("output.txt", "wb")  # create a text output
    for page in pymupdf.open(doc_dir):  # iterate the document pages
        blocks = page.get_text("blocks")  # Get text blocks with positions

        # .encode("utf8")  # get plain text (is in UTF-8)
        doc += page.get_text()
    # out.close()
    print(doc)


def main():

    # local llm
    local_llm()
    return
    # document parsing
    read_document("ocr/Narrative-As-Virtual-Reality.pdf")

    return
# tts systems
    tts = init_tts()

    eg = "hey, it's me: mark cousins dot wav. i'm here to tell you about movies and shit."
    i = 0
    parsed_text = parse(eg)
    print("Recieved", len(parsed_text), "parsed slices")
    for text in parsed_text:
        i += 1
        print("Running slice", i)
        run_tts(tts=tts, text=text,
                output="out/{i}.wav".format(i=i))

    return
# other shit for running later
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


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    main()
