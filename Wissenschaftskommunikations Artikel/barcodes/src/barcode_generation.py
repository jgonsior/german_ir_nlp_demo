import json

import datetime
import platform
import os
import subprocess

import cairo
import jinja2

INVERTED_INDEX_PATH = '../invIndex/'

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


def and_lists(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length")
    return [a & b for a, b in zip(list1, list2)]


def get_xor_and(dict_codes: dict) -> list:
    lst_keys = list(dict_codes.keys())
    if len(dict_codes) == 1:
        print(
            "You only provided one or zero question barcodes or document barcodes, the logic for "
            "shortening them will be skipped!"
        )
        return dict_codes[lst_keys[0]]
    elif len(dict_codes) == 0:
        raise ValueError(
            "You must provide at least one question barcode and document barcode"
        )

    for idx, barcode in enumerate(dict_codes):
        if idx == 0:
            and_barcode = and_lists(dict_codes[barcode], dict_codes[lst_keys[idx + 1]])
        elif idx == len(dict_codes) - 2:
            and_barcode = and_lists(and_barcode, dict_codes[lst_keys[idx + 1]])
        elif idx < len(dict_codes) - 3:
            and_barcode = and_lists(and_barcode, dict_codes[lst_keys[idx + 1]])

    return and_barcode


def remove_redundant(dict_codes: dict, lst_xor: list) -> dict:
    for idx, num_xor in enumerate(lst_xor):
        for barcode in dict_codes:
            if num_xor == 1:
                code = dict_codes[barcode]
                code[idx] = ""
                dict_codes[barcode] = code

    for barcode in dict_codes:
        dict_codes[barcode] = [i for i in dict_codes[barcode] if i != ""]

    return dict_codes


def fill_remaining_zeros(lst, result, max_length, ones_positions):
    if len(result) < max_length:
        if not ones_positions:
            result.extend([0] * (max_length - len(result)))
        else:
            last_one_index = ones_positions[-1]
            remaining_slots = max_length - len(result)
            for i in range(last_one_index + 1, len(lst)):
                if lst[i] == 0 and remaining_slots > 0:
                    result.append(0)
                    remaining_slots -= 1
                if len(result) >= max_length:
                    break

    return result


def barcode_minification(dict_codes: dict, max_length: int) -> dict:
    for code in dict_codes:
        lst = dict_codes[code]
        result = []
        zero_count = 0
        ones_positions = [i for i, x in enumerate(lst) if x == 1]

        ones_count = len(ones_positions)
        max_zeros = (
            (max_length - ones_count) // (ones_count - 1)
            if ones_count > 1
            else max_length - 1
        )

        for num in lst:
            if num == 1:
                result.append(num)
                zero_count = 0
            else:
                zero_count += 1
                if zero_count <= max_zeros:
                    result.append(num)

            if len(result) >= max_length:
                break

        if result.count(1) < ones_count:
            result = []
            zero_count = 0
            for i, num in enumerate(lst):
                if num == 1:
                    result.append(num)
                    zero_count = 0
                else:
                    zero_count += 1
                    if zero_count <= max_zeros:
                        result.append(num)
                if len(result) >= max_length:
                    break

        if len(result) < max_length:
            if ones_positions and ones_positions[-1] >= len(result):
                result.extend([0] * (max_length - len(result)))
            else:
                result = fill_remaining_zeros(
                    lst, result, max_length, ones_positions
                )

        dict_codes[code] = result

    return dict_codes


def draw_svg(name: str, barcode: list, identity: str):
    with cairo.SVGSurface(
        f"../barcodes_out/{identity}s/svg/{identity}_{name}.svg",
        (len(barcode) * 10),
        1000,
    ) as surface:
        context = cairo.Context(surface)
        for idx, numeral in enumerate(barcode):
            if numeral == 0:
                context.set_source_rgb(0, 0, 0)
                context.rectangle(idx * 10, 0, 10, 100)
                context.fill_preserve()
                context.set_source_rgb(1, 1, 1)
                context.set_line_width(2)
                context.stroke()
            else:
                context.set_source_rgb(1, 0.84, 0.3)
                context.rectangle(idx * 10, 0, 10, 100)
                context.fill_preserve()
                context.set_source_rgb(1, 1, 1)
                context.set_line_width(2)
                context.stroke()


def create_latex():
    svg_path_documents = r"../barcodes_out/documents/svg/"
    lst_documents = []
    for file in os.listdir(svg_path_documents):
        file_name, _ = file.split(".")
        lst_documents.append(f"../barcodes_out/documents/svg/{file_name}")

    svg_path_questions = r"../barcodes_out/questions/svg/"
    lst_questions = []
    for file in os.listdir(svg_path_questions):
        file_name, _ = file.split(".")
        lst_questions.append(f"../barcodes_out/questions/svg/{file_name}")

    document_template = latex_jinja_env.get_template("document_stub.tex")
    result_document = document_template.render(lst_documents=lst_documents)

    with open(
        f"../barcodes_out/documents/tex/documents.tex",
        "w",
    ) as file:
        file.write(result_document)

    question_template = latex_jinja_env.get_template("question_stub.tex")
    result_question = question_template.render(lst_questions=lst_questions)

    with open(
        f"../barcodes_out/questions/tex/questions.tex",
        "w",
    ) as file:
        file.write(result_question)


def create_pdf(switch: str):
    folder_path = f'../barcodes_out/{switch}/tex'
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
    subprocess.run([script_path, folder_path], check=True)


def generate_barcodes(
    index_file: str,
    questions_file: str,
    amount: int,
    mode: str,
    max_length: int,
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
        lst_question = questions[question].lower().split()
        for word in inv_index:
            if word in lst_question:
                dict_questions[question].append(1)
            else:
                dict_questions[question].append(0)

    and_barcode_doc = get_xor_and(dict_barcodes) # TODO: instead of xor do and - invert - and to find all 0 or all 1
    dict_barcodes = remove_redundant(dict_barcodes, and_barcode_doc)

    dict_barcodes = barcode_minification(dict_barcodes, max_length)
    dict_questions = barcode_minification(dict_questions, max_length)

    print("Done generating barcodes...")
    print("Generating svg files...")
    if mode == "single":
        for idx, barcode in enumerate(dict_barcodes):
            print(f"Drawing SVG for barcode {barcode}")
            draw_svg(barcode, dict_barcodes[barcode], "document")
            if amount == idx:
                break

        for idx, question in enumerate(dict_questions):
            print(f"Drawing SVG for question {question}")
            draw_svg(question, dict_questions[question], "question")
            if amount == idx:
                break
    else:
        for idx, barcode in enumerate(dict_barcodes):
            print(f"Drawing SVG for barcode {barcode}")
            draw_svg(barcode, dict_barcodes[barcode], "document")

        for idx, question in enumerate(dict_questions):
            print(f"Drawing SVG for question {question}")
            draw_svg(question, dict_questions[question], "question")
    print("Done generating svg files...")
    print("Generating TEX files...")
    create_latex()
    print("Done generating TEX files...")
    print("Generating PDF files from TEX files...")
    create_pdf('documents')
    create_pdf('questions')
    print("Done generating PDF...")
    print("DONE")


if __name__ == "__main__":
    amount = 8
    mode = "single"
    if len(os.listdir(INVERTED_INDEX_PATH)) < 2:
        raise Exception("No inverted index or question files found. Please provide both in JSON format")

    for file in os.listdir(INVERTED_INDEX_PATH):
        if file.endswith(".json"):
            if "questions" not in file:
                index_path = f"../invIndex/{file}"
            else:
                questions_path = f"../invIndex/{file}"
        else:
            raise Exception(f"File type {os.path.splitext(file)} not supported")

    generate_barcodes(index_path, questions_path, amount, mode, max_length=100)
