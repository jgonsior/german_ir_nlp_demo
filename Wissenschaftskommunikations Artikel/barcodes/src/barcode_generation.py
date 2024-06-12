import json

import datetime
import platform
import os
import subprocess
import random

import nltk
import spacy
import cairo
import jinja2

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

nltk.download("stopwords")
stemmer = SnowballStemmer("german")
stop_words = set(stopwords.words("german"))
nlp = spacy.load("de_core_news_sm")

latex_jinja_env = jinja2.Environment(
    block_start_string=r"\BLOCK{",
    block_end_string="}",
    variable_start_string=r"\VAR{",
    variable_end_string="}",
    comment_start_string=r"\#{",
    comment_end_string="}",
    line_statement_prefix="#",
    line_comment_prefix="%#",
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.relpath("../template/")),
)


def detect_os():
    os_name = platform.system()
    print(f"Detected OS: {os_name}")
    return os_name


def draw_svg(name: str, barcode: list, identity: str, height: int, width: int):
    if not os.path.exists(f"../barcodes_out/{identity}/svg/"):
        os.makedirs(f"../barcodes_out/{identity}/svg/")
        print(
            f"created directory: ../barcodes_out/{identity}/svg/ to save the latex file to"
        )

    if len(identity) == 9:
        identity_short = identity[:8]
    else:
        identity_short = identity

    with cairo.SVGSurface(
        f"../barcodes_out/{identity}/svg/{identity_short}_{name}.svg",
        (len(barcode) * width),
        height,
    ) as surface:
        context = cairo.Context(surface)
        for idx, numeral in enumerate(barcode):
            if numeral == 0:
                context.set_source_rgb(0, 0, 0)
                context.rectangle(idx * width, 0, width, height)
                context.fill_preserve()
                context.set_source_rgb(1, 1, 1)
                context.set_line_width(2)
                context.stroke()
            else:
                context.set_source_rgb(1, 0.84, 0)
                context.rectangle(idx * width, 0, width, height)
                context.fill_preserve()
                context.set_source_rgb(1, 1, 1)
                context.set_line_width(2)
                context.stroke()


def create_latex(switch: str):
    pdf_path_files = f"../barcodes_out/{switch}/svg/"
    lst_file = []
    for file in os.listdir(pdf_path_files):
        file_name, _ = file.split(".")
        lst_file.append(file_name)

    lst_file = sorted(lst_file)
    document_template = latex_jinja_env.get_template(f"{switch}_stub.tex")
    result_document = document_template.render(lst_files=lst_file)

    if not os.path.exists(f"../barcodes_out/{switch}/tex"):
        os.makedirs(f"../barcodes_out/{switch}/tex")
        print(
            f"created directory: ../barcodes_out/{switch}/tex to save the latex file to"
        )

    with open(
        f"../barcodes_out/{switch}/tex/{switch}.tex",
        "w",
    ) as document_file:
        document_file.write(result_document)


def create_pdf(switch: str):
    folder_path = f"../barcodes_out/{switch}/tex"
    output_path = f"../barcodes_out/{switch}/pdf"

    if not os.path.exists(f"../barcodes_out/{switch}/pdf/"):
        os.makedirs(f"../barcodes_out/{switch}/pdf/")
        print(
            f"created directory: ../barcodes_out/{switch}/pdf/ to save the pdf files to"
        )

    os_name = detect_os()

    if os_name == "Linux" or os_name == "Darwin":  # Linux or MacOS
        script_name = "run_pdflatex.sh"
    elif os_name == "Windows":
        script_name = "run_pdflatex.bat"
    else:
        raise ValueError("Unsupported Operating System")

    script_path = os.path.join(os.getcwd(), script_name)

    # Make sure the script is executable (only for Unix-like systems)
    if os_name != "Windows":
        subprocess.run(["chmod", "+x", script_path], check=True)

    # Run the script with the folder path as an argument
    subprocess.run([script_path, folder_path, output_path], check=True)


def generate_dummy():
    if not os.path.exists(f"../barcodes_out/dummy/tex/"):
        os.makedirs(f"../barcodes_out/dummy/tex/")
        print(f"created directory: ../barcodes_out/dummy/tex/ to save the pdf files to")
    if not os.path.exists(f"../barcodes_out/dummy/pdf/"):
        os.makedirs(f"../barcodes_out/dummy/pdf/")
        print(f"created directory: ../barcodes_out/dummy/pdf/ to save the pdf files to")

    barcode = [random.choice([0, 1]) for _ in range(20)]

    draw_svg("dummy", barcode, "dummy", 500, 30)


def generate_barcodes(
    index_file: str,
    questions_file: str,
    dimension_file: str,
    answer_file: str,
    amount: int,
    mode: str,
):
    """

    :param max_length:
    :param index_file:
    :param questions_file:
    :param amount:
    :param mode:
    :return:
    """

    dict_questions = {}
    dict_barcodes = {}

    print(f"{datetime.datetime.now()}")
    print("Loading files...")
    with open(index_file, "r", encoding="utf8") as infile:
        inv_index = json.load(infile)
    with open(questions_file, "r", encoding="utf8") as infile:
        questions = json.load(infile)

    if dimension_file:
        with open(dimension_file, "r", encoding="utf8") as infile:
            dimensions = json.load(infile)
    if answer_file:
        with open(answer_file, "r", encoding="utf8") as infile:
            answers = json.load(infile)
    print("Done loading files...")
    print("Generating barcodes...")

    for word in inv_index:
        for doc in inv_index[word]:
            if doc not in dict_barcodes:
                dict_barcodes[doc] = []
        for question in questions:
            if question not in dict_questions:
                dict_questions[question] = []

    for word in inv_index:
        lst_keys = list(dict_barcodes.keys())
        for doc in inv_index[word]:
            dict_barcodes[doc].append(1)
            lst_keys.remove(doc)
        for key in lst_keys:
            dict_barcodes[key].append(0)

    for question in questions:
        questions[question] = questions[question].replace("?", "")

        question_raw = set(
            str(token.lemma_.lower()) for token in nlp(questions[question])
        )
        question_raw = set(
            str(token.lemma_.lower()) for token in nlp(" ".join(question_raw))
        )
        question_token = [
            stemmer.stem(token) for token in question_raw if token not in stop_words
        ]
        question_token = [
            stemmer.stem(token) for token in question_token if token not in stop_words
        ]

        for word in inv_index:
            if word in question_token:
                dict_questions[question].append(1)
            else:
                dict_questions[question].append(0)

    dict_codes = {}
    lst_para = []
    for collection in dict_barcodes:
        if collection in lst_para:
            dict_codes[collection] = dict_barcodes[collection]

    if not os.path.isfile(f"../barcodes_out/dummy/svg/dummy.svg"):
        print("Generating dummy barcode...")
        generate_dummy()
        print("Done generating dummy barcode...")

    print("Done generating barcodes...")

    print("Generating svg files...")
    if mode == "single":
        for idx, barcode in enumerate(dict_barcodes):
            print(f"Drawing SVG for barcode {barcode}")
            draw_svg(barcode, dict_barcodes[barcode], "documents", 100, 10)
            if amount == idx:
                break

        for idx, question in enumerate(dict_questions):
            print(f"Drawing SVG for question {question}")
            draw_svg(question, dict_questions[question], "questions", 100, 10)
            if amount == idx:
                break
    else:
        for idx, barcode in enumerate(dict_barcodes):
            print(f"Drawing SVG for barcode {barcode}")
            draw_svg(barcode, dict_barcodes[barcode], "documents", 100, 10)

        for idx, question in enumerate(dict_questions):
            print(f"Drawing SVG for question {question}")
            draw_svg(question, dict_questions[question], "questions", 100, 10)
    print("Done generating svg files...")
    print("Generating TEX files...")
    create_latex("documents")
    create_latex("questions")
    print("Done generating TEX files...")
    print("Generating PDF files from TEX files...")
    create_pdf("documents")
    create_pdf("questions")
    print("Done generating PDF...")
    print("DONE")


def handler(amount: int, mode: str):
    if len(os.listdir("../invIndex/")) < 2:
        raise Exception(
            "No inverted index, question or dimension files found."
            "Please provide all three in JSON format as specified in the README.md!"
        )

    for file in os.listdir("../invIndex/"):
        if file.endswith(".json"):
            file_name = os.path.splitext(file)[0]
            if file_name.lower() in ["invindex", "inverted_index", "inv_index"]:
                print("Found index file.")
                index_path = f"../invIndex/{file}"
            elif file_name.lower() in [
                "questions",
                "questions_index",
                "questions_index",
            ]:
                print("Found questions file.")
                questions_path = f"../invIndex/{file}"
            elif file_name.lower() in [
                "dimension",
                "dimensions",
                "dimensions_index",
            ]:
                print("Found dimension file.")
                dimensions_path = f"../dimensions/{file}"
            elif file_name.lower() in ["paragraphs", "answers", "answer_paragraphs"]:
                print("Found paragraphs file.")
                answers_path = f"../answers/{file}"
            else:
                print(
                    "Warning a file was found that does not fit the naming scheme provided!"
                )
                print(f"Skipping the file: {file}! Please check if this is correct")
        else:
            raise Exception(
                f"File type {os.path.splitext(file)} not supported! Please provide the files in JSON format"
            )

    if "answers_path" not in locals():
        answers_path = ""
    if "dimensions_path" not in locals():
        dimensions_path = ""

    if "questions_path" or "index_path" not in locals():
        raise Exception(
            "No questions or inverted index found in files! These files are needed in "
            "order to generate the barcodes!"
        )

    generate_barcodes(
        index_path, questions_path, dimensions_path, answers_path, amount, mode
    )


if __name__ == "__main__":
    handler(8, "")
