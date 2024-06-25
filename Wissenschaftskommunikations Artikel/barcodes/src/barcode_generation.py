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


def randomized_list_extension(
    lst_dimensions: list, lst_words: list, amount: int
) -> list:
    unique_elements = set(lst_dimensions)

    while len(lst_dimensions) % amount != 0:
        next_element = random.choice(lst_words)

        if next_element not in unique_elements:
            lst_dimensions.append(next_element)
            unique_elements.add(next_element)

    lst_dimensions = sorted(lst_dimensions)

    return lst_dimensions


def get_stemmed_list(tokens: str) -> list:
    token_raw = set(str(token.lemma_.lower()) for token in nlp(tokens))
    token_raw = set(str(token.lemma_.lower()) for token in nlp(" ".join(token_raw)))
    lst_token = [stemmer.stem(token) for token in token_raw if token not in stop_words]
    lst_token = [stemmer.stem(token) for token in lst_token if token not in stop_words]

    return lst_token


def draw_svg(name: str, barcode: list, identity: str, height: int, width: int):
    if not os.path.exists(f"../barcodes_out/{identity}/svg/"):
        os.makedirs(f"../barcodes_out/{identity}/svg/")
        print(
            f"created directory: ../barcodes_out/{identity}/svg/ to save the latex file to"
        )

    if len(identity) == 9:
        identity_short = identity[:8]
        if identity_short == "question":
            identity_short = "barcode_question"
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


def create_latex(switch: str, dimensions=None, dummy=None):
    pdf_path_files = f"../barcodes_out/{switch}/svg/"
    lst_file = []
    for file in os.listdir(pdf_path_files):
        file_name, _ = file.split(".")
        lst_file.append(file_name)

    if dimensions is not None and dummy is not None:
        lst_file = sorted(lst_file)
        document_template = latex_jinja_env.get_template(f"{switch}_stub.tex")
        result_document = document_template.render(
            file=lst_file[0], dimensions=dimensions, dummy=dummy
        )
    else:
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


def generate_dummy(dimension: int) -> list:
    barcode = [random.choice([0, 1]) for _ in range(dimension)]

    return barcode


def create_dimension_codes(
    index: dict, questions: dict, dimensions: list
) -> tuple[dict, dict]:
    dict_barcodes = {}
    dict_questions = {}

    for word in dimensions:
        for doc in index[word]:
            if doc not in dict_barcodes:
                dict_barcodes[doc] = []

    for question in questions:
        if question not in dict_questions:
            dict_questions[question] = []

    for word in dimensions:
        lst_keys = list(dict_barcodes.keys())
        for doc in index[word]:
            dict_barcodes[doc].append(1)
            lst_keys.remove(doc)
        for key in lst_keys:
            dict_barcodes[key].append(0)

    for question in questions:
        question_string = questions[question].replace("?", "")
        question_token = get_stemmed_list(question_string)

        for word in dimensions:
            if word in question_token:
                dict_questions[question].append(1)
            else:
                dict_questions[question].append(0)

    return dict_barcodes, dict_questions


def generate_barcodes(
    index_file: str,
    questions_file: str,
    dimension_file: str,
    answer_file: str,
    amount: int,
    mode: str,
):
    """

    Args:
        index_file:
        questions_file:
        dimension_file:
        answer_file:
        amount:
        mode:

    Returns:

    """

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

    if not dimensions:
        dict_barcodes, dict_questions = create_dimension_codes(
            inv_index, questions, list(inv_index.keys())
        )
        lst_dimensions = randomized_list_extension([], list(inv_index.keys()), 30)
        dummy = generate_dummy(30)
    else:
        lst_dimensions = list(dimensions.values())
        for ind, dim in enumerate(lst_dimensions):
            if dim == "Status":
                word = "statu"
            elif dim not in ["existiert", "Hogwarts"]:
                word = get_stemmed_list(dim)[0]
            else:
                word = dim.lower()
            lst_dimensions[ind] = word

        lst_dimensions = randomized_list_extension(
            lst_dimensions, list(inv_index.keys()), 100
        )
        dict_barcodes, dict_questions = create_dimension_codes(
            inv_index, questions, lst_dimensions
        )
        dummy = generate_dummy(len(lst_dimensions))

    if answers:
        lst_doc = []
        for doc in inv_index:
            lst_doc.extend(inv_index[doc])

        lst_para = randomized_list_extension(
            list(answers.values()), list(set(lst_doc)), 17
        )

        dict_answers = {}
        for collection in dict_barcodes:
            if collection in lst_para:
                dict_answers[collection] = dict_barcodes[collection]
        dict_barcodes = dict_answers

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

        print("Drawing SVG for the dummy barcode...")
        draw_svg("dummy", dummy, "dummy", 500, 30)
    else:
        for idx, barcode in enumerate(dict_barcodes):
            print(f"Drawing SVG for barcode {barcode}")
            draw_svg(barcode, dict_barcodes[barcode], "documents", 100, 10)

        for idx, question in enumerate(dict_questions):
            print(f"Drawing SVG for question {question}")
            draw_svg(question, dict_questions[question], "questions", 100, 10)

        print("Drawing SVG for the dummy barcode...")
        draw_svg("dummy", dummy, "dummy", 500, 30)
    print("Done generating svg files...")
    for switch in ["documents", "questions", "dummy"]:
        print(f"Generating TEX files for {switch}!")
        if switch == "dummy":
            create_latex("dummy", dimensions=lst_dimensions, dummy=dummy)
        else:
            create_latex(switch)
        print("Done generating TEX files...")
        print(f"Generating PDF files from TEX files for {switch}")
        create_pdf(switch)
        print(f"Done generating PDF for {switch}!")

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
                dimensions_path = f"../invIndex/{file}"
            elif file_name.lower() in ["paragraphs", "answers", "answer_paragraphs"]:
                print("Found paragraphs file.")
                answers_path = f"../invIndex/{file}"
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

    for switch in ["documents", "questions", "dummy"]:
        if os.path.exists(f"../barcodes_out/{switch}/svg/"):
            if len(os.listdir(f"../barcodes_out/{switch}/svg/")) != 0:
                for file in os.listdir(f"../barcodes_out/{switch}/svg/"):
                    os.remove(f"../barcodes_out/{switch}/svg/" + file)

    generate_barcodes(
        index_path, questions_path, dimensions_path, answers_path, amount, mode
    )


if __name__ == "__main__":
    handler(8, "")
