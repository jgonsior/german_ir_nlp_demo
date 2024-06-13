def read_text(query_file):
    with open(query_file, "r", encoding="utf-8") as file:
        queries = file.readlines()

    generate_latex_card(queries)


def generate_latex_card(queries):
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write the LaTeX document preamble
        f.write(r'\documentclass[20pt]{memoir}' + '\n')
        f.write(r'\usepackage[utf8]{inputenc}' + '\n')
        f.write(r'\usepackage{graphicx}' + '\n')
        f.write(r'\usepackage{geometry}' + '\n')
        f.write(r'\usepackage{fontspec}' + '\n')
        f.write(r'\usepackage{svg}' + '\n')
        f.write(r'\usepackage{moresize}' + '\n')
        f.write(r'\geometry{paperwidth=210mm, paperheight=148.5mm, left=14mm, right=14mm, top=0mm, bottom=0mm}' + '\n')
        f.write(r'\setmainfont{parambol (1).ttf}' + '\n')
        f.write(r'\begin{document}' + '\n')
        f.write(r'\thispagestyle{empty}' + '\n')
        f.write(r'\begin{center}' + '\n')

        counter = 0

        for question in queries:
            # barcode
            f.write(r'\includesvg[scale=0.460]{barcodes/barcode_question_' + str(counter + 1) + '.svg}' + '\n')
            f.write(r'\begin{vplace}[1]' + '\n')
            # question
            f.write(r'{\HUGE ' + question + '}' + '\n')
            f.write(r'\end{vplace}' + '\n')

            # embedding
            f.write(r'\includesvg[scale=0.45]{embeddings/question_' + str(counter) + '.svg}' + '\n')

            f.write(r'\newpage' + '\n')
            counter = counter + 1

        f.write(r'\end{center}' + '\n')
        f.write(r'\end{document}' + '\n')


def main(input_file, output_file):
    read_text(input_file)
    # Now you can use 'queries' for further processing


if __name__ == "__main__":
    input_file = "res/queries/queries.txt"
    output_file = "res/queries/testcard.tex"
    main(input_file, output_file)
