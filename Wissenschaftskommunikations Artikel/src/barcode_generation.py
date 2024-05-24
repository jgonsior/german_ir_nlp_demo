import json

import datetime
import math

import cairo
import jinja2
import os

latex_jinja_env = jinja2.Environment(
    block_start_string=r'\BLOCK{',
    block_end_string='}',
    variable_start_string=r'\VAR{',
    variable_end_string='}',
    comment_start_string=r'\#{',
    comment_end_string='}',
    line_statement_prefix='#',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.relpath('../template/'))
)


def draw_svg(name: str, dict_draw: dict, identity: str):
    for code_seq in dict_draw:
        with cairo.SVGSurface(f'../barcodes_out/{identity}s/svg/{identity}_{name}_{code_seq}.svg',
                              (len(dict_draw[code_seq]) * 10), 1000) as surface:
            context = cairo.Context(surface)
            for idx, numeral in enumerate(dict_draw[code_seq]):
                if numeral == 0:
                    context.set_source_rgb(0, 0, 0.6)
                    context.rectangle(idx * 10, 0, 10, 500)
                    # context.fill()
                    context.fill_preserve()
                    context.set_source_rgb(1, 1, 1)
                    context.set_line_width(2)
                    context.stroke()
                else:
                    context.set_source_rgb(0, 0, 0)
                    context.rectangle(idx * 10, 0, 10, 500)
                    # context.fill()
                    context.fill_preserve()
                    context.set_source_rgb(1, 1, 1)
                    context.set_line_width(2)
                    context.stroke()


def get_divided_code(code: list, divider: int) -> dict:
    dict_code = {}
    for i in range(divider):
        if i == 0:
            upper_bound = math.floor(len(code) / divider)
            print(i, upper_bound)
            dict_code[i] = code[0:upper_bound]
        elif i == divider - 1:
            lower_bound = math.ceil((len(code) / divider) * i)
            print(i, lower_bound)
            dict_code[i] = code[lower_bound::]
        else:
            lower_bound = math.ceil((len(code) / divider) * i)
            upper_bound = math.floor((len(code) / divider) * (i + 1))
            print(i, lower_bound, upper_bound)
            dict_code[i] = code[lower_bound:upper_bound]

    return dict_code


def create_latex(dict_barcodes: dict, dict_questions: dict, mode: str, amount: int, divider: int):
    if mode == 'single':
        for idx, barcode in enumerate(dict_barcodes):
            print(f'Drawing SVG for barcode {barcode}')
            if divider <= 1:
                draw_svg(barcode, {"1": dict_barcodes[barcode]}, "document")
            else:
                dict_code = get_divided_code(dict_barcodes[barcode], divider)
                length = 0
                for i in dict_code:
                    length += len(dict_code[i])
                print(len(dict_barcodes[barcode]), length)
                draw_svg(barcode, dict_code, "document")

            barcode_template = latex_jinja_env.get_template('barcode_single_stub.tex')
            result_barcode = barcode_template.render(barcode=dict_barcodes[barcode], barcode_name=barcode)
            with open(f'../barcodes_out/documents/tex/barcode_{barcode}.tex', 'w') as file:
                file.write(result_barcode)

            if idx == amount:
                break

        for idx, question in enumerate(dict_questions):
            print(f'Drawing SVG for question {question}')
            if divider > 1:
                dict_code = get_divided_code(dict_questions[question], divider)
                length = 0
                for i in dict_code:
                    length += len(dict_code[i])
                print(len(dict_questions[question]), length)
                draw_svg(question, dict_code, "question")
            else:
                draw_svg(question, {"1": dict_questions[question]}, "question")

            question_template = latex_jinja_env.get_template('question_single_stub.tex')
            result_question = question_template.render(question=dict_questions[question], question_name=question)
            with open(f'../barcodes_out/questions/tex/question_{question}.tex', 'w') as file:
                file.write(result_question)

            if idx == amount:
                break
    else:
        barcode_template = latex_jinja_env.get_template('barcode_stub.tex')
        result_barcode = barcode_template.render(dict_barcodes=dict_barcodes)

        question_template = latex_jinja_env.get_template('question_stub.tex')
        result_question = question_template.render(dict_questions=dict_questions)

        with open('../template/question.tex', 'w') as file:
            file.write(result_question)
        with open('../template/barcode.tex', 'w') as f:
            f.write(result_barcode)


def generate_barcodes(index_file: str, questions_file: str, divider: int, amount: int = 5, mode: str = 'single'):
    dict_questions = {}
    dict_barcodes = {}

    print(f'{datetime.datetime.now()}')
    print('Loading files...')
    with open(index_file, 'r', encoding='utf8') as infile:
        inv_index = json.load(infile)
    with open(questions_file, 'r', encoding='utf8') as infile:
        questions = json.load(infile)

    print('Done loading files...')
    print('Generating barcodes...')

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
        for word in inv_index:
            lst_question = questions[question].split()
            if word in lst_question:
                dict_questions[question].append(1)
            else:
                dict_questions[question].append(0)

    print('Done generating barcodes...')
    print('Generating files...')
    create_latex(dict_barcodes, dict_questions, mode, amount, divider)
    print('Done generating files...')


if __name__ == "__main__":
    amount = 5
    mode = 'single'
    index_path = '../invIndex/inv_index_Harry.json'
    questions_path = '../invIndex/questions.json'
    generate_barcodes(index_path, questions_path, divider=4)
