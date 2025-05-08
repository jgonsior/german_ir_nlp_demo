import glob
import re
import os
from pathlib import Path


def add_absatz_comment(input_text):
    """
    Adds a %ABSATZ comment after every \newline command in the LaTeX document.
    This will be used for enumerating the documents and displaying section numbers in latex
    Some %ABSATZ comments have been already added manually, if not separated by newline


    Parameters:
    input_text (str): The input LaTeX document as a string.

    Returns:
    str: The modified LaTeX document with %ABSATZ comments added.
    """
    output_text = ""
    inside_document = False

    # Split the input text by \newline to process each section separately
    sections = re.split(r"(\\newline)", input_text)

    for section in sections:
        if not inside_document and "\\begin{document}" in section:
            inside_document = True

        if inside_document:
            if section.strip() == "\\newline":
                # Add %ABSATZ comment after each \newline
                output_text += f"{section}\n%ABSATZ "
            else:
                output_text += section
        else:
            output_text += section

    return output_text


def replace_absatz(added_text):
    """
    Replaces %ABSATZ comments with marginpar{} commands to enumerate the sections.
    Will display number next to latex text
    Also needed later for the inverted index to determine the sections

    Parameters:
    added_text (str): The input LaTeX document with %ABSATZ comments.

    Returns:
    str: The modified LaTeX document with marginpar{} commands added.
    """
    section_counter = 1
    output_text = ""
    inside_document = False

    # Split the input text by %ABSATZ to process each section separately
    sections = re.split(r"(%ABSATZ)", added_text)

    for section in sections:
        if not inside_document and "\\begin{document}" in section:
            inside_document = True

        if inside_document:
            if section.strip() == "%ABSATZ":
                # Add \marginpar with the section number after each %ABSATZ
                output_text += f"\\marginpar{{{section_counter}}} "
                section_counter += 1  # Increment the section counter
            else:
                output_text += section
        else:
            output_text += section

    return output_text

def main(input_file, output_file):
    """
    Reads the input file, processes it to add %ABSATZ comments and marginpar{} commands
    and writes the output to the specified file.
    """

    with open(input_file, "r") as f:
        input_text = f.read()  # Read the input file content

    # Add %ABSATZ comments to the input text
    added_text = add_absatz_comment(input_text)
    # Replace %ABSATZ comments with \marginpar{} commands
    output_text = replace_absatz(added_text)

    # Write the processed content to the output file
    with open(output_file, "w") as f:
        f.write(output_text)


def _ensure_directory_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        if os.path.isdir(path):
            print(f"Directory already exists: {path}")
        else:
            print(f"A file with the same name exists: {path}")

if __name__ == "__main__":
    # Get the base directory of the script
    BASE_DIR = Path(__file__).parent

    print(f"Base directory: '{BASE_DIR}'")

    # Find all .tex files in the specified directory
    documents = sorted((BASE_DIR / "src" / "files" / "raw").glob("*.tex"))
    print(f"Found documents: {[doc.name for doc in documents]} in '{documents[0].parent}'")

    # Define the output directory
    ENUMERATED_DIR = BASE_DIR / "src" / "files" / "enumerated"
    print(f"Enumerated directory path: '{ENUMERATED_DIR}'")
    _ensure_directory_exists(ENUMERATED_DIR)

    # Process each .tex file found
    for input_file in documents:

        # Construct the output file path using the absolute path of ENUMERATED_DIR
        output_file = ENUMERATED_DIR / input_file.name.replace(".tex", "_enumerated.tex")

        main(input_file, output_file)
        print(f"Processed {input_file.name} and created {output_file.name}")