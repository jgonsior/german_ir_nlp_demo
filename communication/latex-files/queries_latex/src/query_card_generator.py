import re


# Read the queries from the input file
def read_text(query_file):
    with open(query_file, "r", encoding="utf-8") as file:
        queries = file.readlines()

    return queries


# Generate LaTeX document for query cards in A5 format
def generate_latex_card(queries, output_file):
    """
    Generates a LaTeX document for printing query cards in A5 format.
    Each card includes a question, barcode, embedding, and an image based on difficulty on its backside.
    To support double printing, it first generates two questions (front) then two images (back).
    Merging of the A5 cards to A4 has to be done manually

    Args:
    - queries (list): List of query lines to be processed.
    - output_file (str): Output file path for the generated LaTeX document.
    """
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

        # Process the queries in pairs
        for i in range(0, len(queries), 2):
            if i + 1 < len(queries):  # Ensure there are at least two lines to process
                # Parse the first and second question
                question1, tags1 = parse_question(queries[i].strip())
                question2, tags2 = parse_question(queries[i + 1].strip())

                # Generate LaTeX content for the first question card
                generate_question_card(f, counter, question1, tags1)
                counter += 1

                # Generate LaTeX content for the second question card
                generate_question_card(f, counter, question2, tags2)
                counter += 1

        f.write(r'\end{center}' + '\n')
        f.write(r'\end{document}' + '\n')


# Helper function to parse a question line and extract tags
def parse_question(line):
    """
    Parses a question line and extracts tags indicated by hashtags.

    Args:
    - line (str): A line containing a question with optional hashtags.

    Returns:
    - tuple: A tuple containing the question (str) and a list of tags (list of str).
    """
    tags = re.findall(r'#(\w+)', line)  # Extract tags indicated by hashtags
    question_part = re.sub(r'\s*#\w+', '', line)  # Remove hashtags from the question part
    return question_part.strip(), tags


# Helper function to generate LaTeX content for a question card
def generate_question_card(f, counter, question, tags):
    """
    Generates LaTeX content for a question card including barcode, question text,
    embedding, and an image based on the difficulty level.
    Images (svg and png for the images) have to be provided in LaTex.
    No Loading of image files happens.

    Args:
    - f (file object): File object to write LaTeX content.
    - counter (int): Counter for question numbering.
    - question (str): Question text.
    - tags (list): List of tags indicating difficulty and spoilers.
    """
    f.write(r'\includesvg[scale=0.460]{barcodes/barcode_question_' + str(counter + 1) + '.svg}' + '\n')
    f.write(r'\begin{vplace}[1]' + '\n')
    f.write(r'{\HUGE ' + question + '}' + '\n')
    f.write(r'\end{vplace}' + '\n')
    f.write(r'\includesvg[scale=0.45]{embeddings/question_' + str(counter + 1) + '.svg}' + '\n')
    f.write(r'\newpage' + '\n')

    # Determine the image file based on difficulty and spoiler tags
    image_file = None
    if 'leicht' in tags:
        if 'SPOILER' in tags:
            image_file = "images/q_leicht_spoiler.png"
        else:
            image_file = "images/q_leicht.png"
    elif 'mittel' in tags:
        if 'SPOILER' in tags:
            image_file = "images/q_mittel_spoiler.png"
        else:
            image_file = "images/q_mittel.png"
    elif 'schwer' in tags:
        if 'SPOILER' in tags:
            image_file = "images/q_schwer_spoiler.png"
        else:
            image_file = "images/q_schwer.png"

    if image_file:
        f.write(r'\begin{center}' + '\n')
        f.write(r'\includegraphics[width=1\textwidth]{' + image_file + '}' + '\n')
        f.write(r'\vspace{1cm}' + '\n')  # Adjust vertical space as needed
        f.write(r'\end{center}' + '\n')
        f.write(r'\newpage' + '\n')


def main(input_file, output_file):
    queries = read_text(input_file)
    generate_latex_card(queries, output_file)
