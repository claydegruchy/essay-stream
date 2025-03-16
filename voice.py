
# import argparse
# import sys
from pathlib import Path
import os
print("Imports done")

base_params = {
    "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
    "speaker_wav": "samples/storyoffilm.wav",
    "language_idx": "en",
    "title": ""
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


llm_model_id = "Qwen/Qwen2.5-1.5B"
base_template = """Question: {question}

    Answer: """


def local_llm(question, template=base_template):
    print("Starting local llm")
    from langchain.llms.huggingface_pipeline import HuggingFacePipeline
    hf = HuggingFacePipeline.from_model_id(
        model_id=llm_model_id, task="text-generation", pipeline_kwargs={"max_new_tokens": 200, "pad_token_id": 50256},
    )
    from langchain.prompts import PromptTemplate
    prompt = PromptTemplate.from_template(template)
    chain = prompt | hf

    return chain.invoke({"question": question})


def get_coordinates(doc_dir):
    return


def read_document(doc_dir, job_path):
    # we read the doc into blocks
    # then we use some coordinates to ensure we only get the blocks within an area
    # that we actually want
    import pymupdf
    import random

    # doc = []

    # # out = open("output.txt", "wb")  # create a text output
    # for page in pymupdf.open(doc_dir):  # iterate the document pages
    #     blocks = page.get_text("blocks")  # Get text blocks with positions
    #     doc += [x[4] for x in blocks]
    # return doc
    # from langchain_community.document_loaders import PyPDFLoader

    # loader = PyPDFLoader(doc_dir)
    # pages = []
    # for page in loader.lazy_load():
    #     pages.append(page)
    # print(pages[200].page_content)

    from langchain.text_splitter import MarkdownTextSplitter
    import json
    pre_processed_file = f"{job_path}/pre_processed.md"
    processed_file = f"{job_path}/processed.md"
    if not os.path.exists(processed_file):
        print("processed_file does not exist")
        if not os.path.exists(pre_processed_file):
            print("pre_processed does not exist")
            import pymupdf4llm
            md_text = pymupdf4llm.to_markdown(doc_dir, page_chunks=True)
            dic = ""
            for page in md_text:
                dic += page["text"]

            write_file(pre_processed_file, dic)

        import re
        pattern = r"(.*(||||||||||).*\n\n|\n+-----\n)"

        document = read_file(pre_processed_file)

        match = re.findall(pattern, document)
        print(len(match))
        document = re.sub(pattern, "", document)
        match = re.findall(pattern, document)
        print(len(match))
        if match:
            print("Match found:")
            # for x in match:
            #     print(x)
            print(len(match))
        else:
            print("否 match.")

        print("processing lines for easy consuption")
        n = ""
        for line in document.splitlines():
            if "#" in line:
                n += "\n\n" + line.strip() + "\n"
            else:
                n += line.strip() + " "
        document = n

        print("adding read assist markers")
        changes = [("######", "Subheading:"),
                   ("#####", "Minor Section Title:"),
                   ("####", "Sub-subsection Title:"),
                   ("###", "Subsection Title:"),
                   ("##", "Section Title:"),
                   ("#", "Title:"),
                   ("\*\*\*", ""),
                   ]

        for (pattern, sub) in changes:
            document = re.sub(pattern, sub, document)

        write_file(processed_file, "\n".join(parse(document)))
    document = read_file(processed_file)
    return parse(document)


path_base = "./output/"


def prep_job(job_title):
    print("prep_job", job_title)
    folder_path = Path(path_base+f"{job_title}")
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path


def get_last_file(job_title):
    print("get_last_file", job_title)
    folder_path = Path(path_base+f"{job_title}")
    wav_files = sorted(folder_path.glob("*.wav"))
    if wav_files:
        last_file = wav_files[-1]
        return int(last_file.stem)  # Return just the number (stem)
    return None  # 否 files found


def main():
    start_page = 11
    end_page = 12
    filename = "ocr/Narrative-As-Virtual-Reality.pdf"
    job_title = Path(filename).stem

    path = prep_job(job_title)
    # output making
    # return

    # local llm
    # x = local_llm("how old is the earth?")
    # print(x)
    # return
    # document parsing
    parsed_text = read_document(filename, path)
    # print(len(doc))
    # doc = doc[start_page:end_page+1]

    # print(''.join(doc))
    return

# tts systems

    # start_position = 0
    # end_position = len(parsed_text)-1
    start_position = 3010
    end_position = 3013
    # parsed_text = parsed_text[3001:3010]
    print("Recieved", len(parsed_text), "parsed slices")
    last = get_last_file(job_title)
    if (last):
        print("resuming from last position", last)
        start_position = last
    i = start_position
    print("Processing", end_position-start_position, "items")
    print(path)
    # return
    tts = init_tts()
    for text in parsed_text:
        i += 1
        if i > end_position:
            break
        print("Running slice", i)
        run_tts(tts=tts, text=text,
                output="{path}/{i}.wav".format(i=i, path=path))

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
