import os
import shutil
import json
import html
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
PATH_PDFLATEX = os.getenv("PATH_PDFLATEX")
BOX_WIDTH = os.getenv("BOX_WIDTH")
BOX_SPACING = os.getenv("BOX_SPACING")
FILE_TO_PROCESS = os.getenv("FILE_TO_PROCESS")


def get_cleaned_text(text: str) -> str:
    cleaned_text = html.unescape(text)
    symbols_to_remove = ["[", "]", "(", ")", ",", ".", ":", "„", "“", "'", "&", "-"]
    for symbol in symbols_to_remove:
        cleaned_text = cleaned_text.replace(symbol, "")
    cleaned_text = cleaned_text.replace("  ", " ")
    return cleaned_text

def get_substrings(text, n=5):
    words = text.split()
    substrings = []
    for i in range(len(words) - n + 1):
        substring = ' & '.join(words[i:i+n])
        substrings.append(substring)
    return substrings

if __name__ == '__main__':

    file_dir = os.path.join(FILE_TO_PROCESS)

    with open(file_dir, encoding="utf-8") as file:
        documents = json.load(file)

        for document in documents:
            for i in range(len(document["text"])):
                for template in ["template_wordboxes.tex", "template_tables.tex"]:

                    temporary_template = Path(template).stem + "_temp"

                    shutil.copyfile(template, f"{temporary_template}.tex")

                    with open(f"{temporary_template}.tex", "r+", encoding="utf-8") as temp_file:
                        file_contents = temp_file.read()

                        cleaned_text = get_cleaned_text(document["text"][i])

                        # We write our boxes in main part of the tex file
                        if template == "template_wordboxes.tex":
                            file_contents = file_contents.replace("%box_width%", BOX_WIDTH)

                            document_content = ""
                            for token in cleaned_text.split():
                                document_content += r"\wordbox{" + token + r"} \\ \vspace{" + BOX_SPACING + r"} "
                        else:
                            document_content = ""
                            for pair in get_substrings(cleaned_text):
                                document_content += pair + r"\\"

                        file_contents = file_contents.replace("%document_content%", document_content)

                        # Purge old content and write new
                        temp_file.seek(0)
                        temp_file.truncate()
                        temp_file.write(file_contents)

                    if PATH_PDFLATEX:
                        os.system(f"{PATH_PDFLATEX} {temporary_template}.tex")
                    else:
                        os.system(f"pdflatex {temporary_template}.tex")

                    shutil.move(f"{temporary_template}.pdf", f"output/{Path(template).stem.replace('template_', '')}_{str(i)}.pdf")

                    # We don't need these anymore
                    os.remove(f"{temporary_template}.tex")
                    os.remove(f"{temporary_template}.aux")
                    os.remove(f"{temporary_template}.log")