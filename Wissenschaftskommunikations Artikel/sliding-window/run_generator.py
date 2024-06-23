import os
import shutil
import json
import html
from pathlib import Path
from typing import List

BOX_WIDTH="7.2cm"
BOX_SPACING=".3cm"
FILE_TO_PROCESS="source-material/selected-passages.json"

def get_cleaned_text(text: str) -> str:
    """
    Removes spaces and other symbols that could interrupt the reading flow when looking at each individual word.
    You may need to add some more symbols to `symbols_to_remove` after generation is completed.

    Args:
        text: Text to process

    Returns: Text without any interrupting words

    """
    cleaned_text = html.unescape(text)
    symbols_to_remove = ["[", "]", "(", ")", ",", ".", ":", "„", "“", "”", "'", "&", "’"]
    for symbol in symbols_to_remove:
        cleaned_text = cleaned_text.replace(symbol, "")
    cleaned_text = cleaned_text.replace("  ", " ")
    return cleaned_text

def get_substrings(text: str, n:int=5) -> List[str]:
    """
    Splits a string into a list of subsequent strings with n words concatenated with "&".

    Example:
        text:   "This is a very long string"
        n:      2
        returns ['This & is', 'is & a', 'a & very', 'very & long', 'long & string']

    Args:
        text:   Initial string to be processed
        n:      Number of words to be concatenated

    Returns: List of strings

    """
    words = text.split()
    substrings = []
    for i in range(len(words) - n + 1):
        # The "&" needs to be there for the table to populate the cells in the table accordingly
        substring = ' & '.join(words[i:i+n])
        substrings.append(substring)
    return substrings

if __name__ == '__main__':

    file_dir = os.path.join(FILE_TO_PROCESS)

    with open(file_dir, encoding="utf-8") as file:
        documents = json.load(file)

        doc_count = 0

        # Iterate over every possible text passages
        for i in range(len(documents)):
            document = documents[i]

            for j in range(len(document["text"])):

                # First create the pdf file for the boxes, second for the tables
                for template in ["template_wordboxes.tex", "template_tables.tex"]:

                    doc_count += 1
                    temporary_template = Path(template).stem + "_temp"

                    # We use temporary copies so we do not modify any of our templates we put a lot of effort in
                    shutil.copyfile(f"./source-material/{template}", f"{temporary_template}.tex")

                    with open(f"{temporary_template}.tex", "r+", encoding="utf-8") as temp_file:

                        file_contents = temp_file.read()
                        cleaned_text = get_cleaned_text(document["text"][j])

                        if template == "template_wordboxes.tex":

                            # Replace some placeholders in the template
                            file_contents = file_contents.replace("%box_width%", BOX_WIDTH)

                            document_content = ""
                            # Now we have to create a single box and apply the correct spacing underneath
                            for token in cleaned_text.split():
                                # This will create a very long line but we don't to care, the compiler does neither...
                                document_content += r"\wordbox{" + token + r"} \\ \vspace{" + BOX_SPACING + r"} "
                        else:
                            document_content = ""
                            # Iterate over the table rows
                            for pair in get_substrings(cleaned_text):
                                # Mark the end of the row accordingly
                                document_content += pair + r"\\"

                        # If the json contains an id we can use it
                        if "id" in document:
                            file_contents = file_contents.replace("%letter_increment%", document["id"])
                        # Otherwise we just put the number of the document
                        else:
                            file_contents = file_contents.replace("%letter_increment%", str(doc_count))
                        file_contents = file_contents.replace("%document_content%", document_content)

                        # Purge old content and write new content inside our temporary copy
                        # This needs to be done otherwise the file gets messed up entirely
                        temp_file.seek(0)
                        temp_file.truncate()
                        temp_file.write(file_contents)

                    if template == "template_wordboxes.tex":
                        compiler = "pdflatex"
                    else:
                        # Those tables that can exceed a page need to be run with xelatex, sadly
                        compiler = "xelatex"

                    os.system(f"{compiler} {temporary_template}.tex")

                    # Put the file in the correct location
                    shutil.move(f"{temporary_template}.pdf", f"output/{Path(template).stem.replace('template_', '')}_{str(i)}.pdf")

                    # We don't need these anymore
                    os.remove(f"{temporary_template}.tex")
                    os.remove(f"{temporary_template}.aux")
                    os.remove(f"{temporary_template}.log")