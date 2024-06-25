import glob
import re


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


if __name__ == "__main__":
    # Use glob to find all .tex files in the specified directory
    documents = glob.glob("src/files/raw/*.tex")

    for doc in documents:
        input_file = doc  # Current input file
        # Construct the output file path
        output_file = "src/files/enumerated/" + input_file.replace("\\", "/").split("/")[-1].split(".")[
            0] + "_enumerated.tex"
        # Process the input file and write the output file
        main(input_file, output_file)
