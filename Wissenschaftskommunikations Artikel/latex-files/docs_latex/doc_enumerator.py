import re


def add_absatz_comment(input_text):
    output_text = ""
    inside_document = False

    sections = re.split(r"(\\newline)", input_text)

    for section in sections:
        if not inside_document and "\\begin{document}" in section:
            inside_document = True

        if inside_document:
            if section.strip() == "\\newline":
                # Add %Absatz comment after each \newline
                output_text += f"{section}\n%ABSATZ "
            else:
                output_text += section
        else:
            output_text += section

    return output_text


def replace_absatz(added_text):
    section_counter = 1
    output_text = ""
    inside_document = False

    # Split the input text by %ABSATZ
    sections = re.split(r"(%ABSATZ)", added_text)

    for section in sections:
        # Detect \begin{document} and set flag to true
        if not inside_document and "\\begin{document}" in section:
            inside_document = True

        if inside_document:
            if section.strip() == "%ABSATZ":
                # Add \marginpar after each %ABSATZ
                output_text += f"\\marginpar{{{section_counter}}} "
                section_counter += 1
            else:
                output_text += section
        else:
            output_text += section

    return output_text


def main(input_file, output_file):
    with open(input_file, "r") as f:
        input_text = f.read()

    # Add %Absatz comment to input text
    added_text = add_absatz_comment(input_text)
    output_text = replace_absatz(added_text)

    # Write output tex file
    with open(output_file, "w") as f:
        f.write(output_text)


if __name__ == "__main__":
    # Latex doc is entered manually so far , since only needed for 6 docs
    # could be extended with user input
    documents = ["src/files/raw/Dumbledore.tex", "src/files/raw/HarryPotter.tex",
                 "src/files/raw/Hogwarts.tex",
                 "src/files/raw/Minerva.tex", "src/files/raw/Snape.tex",
                 "src/files/raw/Voldemort.tex"]

    for doc in documents:
        input_file = doc
        output_file = "src/files/enumerated/" + input_file.split("/")[-1].split(".")[0] + "_enumerated.tex"
        main(input_file, output_file)
