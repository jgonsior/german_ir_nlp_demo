import os
import platform
import subprocess
import jinja2

# Configure the Jinja2 environment for LaTeX templates
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
    loader=jinja2.FileSystemLoader(os.path.abspath("Wissenschaftskommunikations Artikel/barcodes/template/")),
)

def detect_os() -> str:
    """
    Detect the operating system of the machine.

    Returns:
        str: The name of the operating system.
    """
    os_name = platform.system()
    print(f"Detected OS: {os_name}")
    return os_name

def create_latex():
    """
    Generate a LaTeX document based on SVG files in a specific directory.

    This function reads SVG files from a predefined directory, processes them using a Jinja2 template,
    and writes the resulting LaTeX code to a new file.
    """
    pdf_path_files = "Wissenschaftskommunikations Artikel/colored barcodes/answers"
    lst_file = sorted([f.split(".")[0] for f in os.listdir(pdf_path_files) if f.endswith(".svg")])

    document_template = latex_jinja_env.get_template("documents_colored_stub.tex")
    result_document = document_template.render(lst_files=lst_file)

    output_dir = "Wissenschaftskommunikations Artikel/colored barcodes/generated barcodes"
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "documents_colored.tex"), "w") as document_file:
        document_file.write(result_document)

def create_pdf():
    """
    Compile a LaTeX document into a PDF file.

    This function detects the operating system, determines the appropriate script to run,
    and executes the script to compile the LaTeX document into a PDF, name the `generated barcodes/latex logs/documents_colored.pdf`.
    It also handles directory creation and setting execute permissions for non-Windows systems.
    """
    folder_path = "Wissenschaftskommunikations Artikel/colored barcodes/generated barcodes"
    output_path = "Wissenschaftskommunikations Artikel/colored barcodes/generated barcodes/latex logs"

    os.makedirs(output_path, exist_ok=True)

    os_name = detect_os()

    if os_name in ["Linux", "Darwin"]:  # Linux or MacOS
        script_name = "Wissenschaftskommunikations Artikel/barcodes/src/run_pdflatex.sh"
    elif os_name == "Windows":
        script_name = "Wissenschaftskommunikations Artikel/barcodes/src/run_pdflatex.bat"
    else:
        raise ValueError("Unsupported Operating System")

    script_path = os.path.join(os.getcwd(), script_name)

    if os_name != "Windows":
        subprocess.run(["chmod", "+x", script_path], check=True)

    subprocess.run([script_path, folder_path, output_path], check=True)

if __name__ == "__main__":
    create_latex()
    create_pdf()
