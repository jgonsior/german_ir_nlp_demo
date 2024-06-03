import json

import datetime
import math
from typing import Tuple

import cairo
import jinja2
import os

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
                context.rectangle(idx * 10, 0, 10, 500)
                context.fill_preserve()
                context.set_source_rgb(1, 1, 1)
                context.set_line_width(2)
                context.stroke()
            else:
                context.set_source_rgb(1, 0.84, 0.3)
                context.rectangle(idx * 10, 0, 10, 500)
                context.fill_preserve()
                context.set_source_rgb(1, 1, 1)
                context.set_line_width(2)
                context.stroke()


def get_divided_code(code: list, divider: int) -> dict:
    dict_code = {}
    for i in range(divider):
        if i == 0:
            upper_bound = math.floor(len(code) / divider) + 1
            dict_code[i] = code[0:upper_bound]
        elif i == divider - 1:
            lower_bound = math.ceil((len(code) / divider) * i)
            dict_code[i] = code[lower_bound::]
        else:
            lower_bound = math.ceil((len(code) / divider) * i)
            upper_bound = math.floor((len(code) / divider) * (i + 1) + 1)
            dict_code[i] = code[lower_bound:upper_bound]

    return dict_code


def xor_lists(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length")
    return [a ^ b for a, b in zip(list1, list2)]


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
            xor_barcode = xor_lists(dict_codes[barcode], dict_codes[lst_keys[idx + 1]])
            and_barcode = and_lists(dict_codes[barcode], dict_codes[lst_keys[idx + 1]])
        elif idx == len(dict_codes) - 2:
            xor_barcode = xor_lists(xor_barcode, dict_codes[lst_keys[idx + 1]])
            and_barcode = and_lists(and_barcode, dict_codes[lst_keys[idx + 1]])
        elif idx < len(dict_codes) - 3:
            xor_barcode = xor_lists(xor_barcode, dict_codes[lst_keys[idx + 1]])
            and_barcode = and_lists(and_barcode, dict_codes[lst_keys[idx + 1]])

    return xor_barcode


def remove_redundant(dict_codes: dict, lst_xor: list) -> dict:
    for idx, num_xor in enumerate(lst_xor):
        for barcode in dict_codes:
            if num_xor == 0:
                code = dict_codes[barcode]
                code[idx] = ""
                dict_codes[barcode] = code

    for barcode in dict_codes:
        dict_codes[barcode] = [i for i in dict_codes[barcode] if i != ""]

    return dict_codes


def fill_remaining_zeros(lst, result, max_length, ones_positions, max_zeros):
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
                    lst, result, max_length, ones_positions, max_zeros
                )

        dict_codes[code] = result

    return dict_codes


def create_latex():
    svg_path_documents = r"../barcodes_out/documents/svg/"
    lst_documents = []
    for file in os.listdir(svg_path_documents):
        file_name, _ = file.split(".")
        lst_documents.append(f"../svg/{file_name}")

    svg_path_questions = r"../barcodes_out/questions/svg/"
    lst_questions = []
    for file in os.listdir(svg_path_questions):
        file_name, _ = file.split(".")
        lst_questions.append(f"../svg/{file_name}")

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
        print(lst_question)
        for word in inv_index:
            print(word)
            if word in lst_question:
                dict_questions[question].append(1)
            else:
                dict_questions[question].append(0)

    xor_barcode_doc = get_xor_and(dict_barcodes)
    dict_barcodes = remove_redundant(dict_barcodes, xor_barcode_doc)

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
    print("DONE")


if __name__ == "__main__":
    amount = 8
    mode = "single"
    index_path = "../invIndex/inv_index_wisschenschaftskommunikation_normalized_summarised.json"
    questions_path = "../invIndex/questions.json"
    generate_barcodes(index_path, questions_path, amount, mode, max_length=100)
