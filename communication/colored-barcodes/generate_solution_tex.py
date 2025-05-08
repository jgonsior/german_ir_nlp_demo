import os
import platform
import subprocess
import jinja2

# PATH SETUP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOADER = os.path.abspath(os.path.join(BASE_DIR, "..", "barcodes", "template"))
PDF_PATH_FILES = os.path.abspath(os.path.join(BASE_DIR, "answers"))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "generated-barcodes"))

LATEX_DIR = OUTPUT_DIR
LOGS = os.path.abspath(os.path.join(OUTPUT_DIR, "logs"))

# Verify paths
# print("Base Directory:", BASE_DIR)
# print("Template Directory:", LOADER)
# print("SVG Files Directory:", PDF_PATH_FILES)
# print("Output Directory:", OUTPUT_DIR)
# print("Logs Directory:", LOGS)

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
    loader=jinja2.FileSystemLoader(LOADER),
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

    lst_file = sorted([f.split(".")[0] for f in os.listdir(PDF_PATH_FILES) if f.endswith(".svg")])

    document_template = latex_jinja_env.get_template("documents_colored_stub.tex")
    result_document = document_template.render(lst_files=lst_file)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(os.path.join(OUTPUT_DIR, "documents_colored.tex"), "w") as document_file:
        document_file.write(result_document)

def create_pdf():
    """
    Compile a LaTeX document into a PDF file.

    This function detects the operating system, determines the appropriate script to run,
    and executes the script to compile the LaTeX document into a PDF, name the `generated barcodes/latex logs/documents_colored.pdf`.
    It also handles directory creation and setting execute permissions for non-Windows systems.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)

    os_name = detect_os()

    if os_name in ["Linux", "Darwin"]:  # Linux or MacOS
        script_name = os.path.join(BASE_DIR, "..", "barcodes", "src", "run_pdflatex.sh")
    elif os_name == "Windows":
        script_name = os.path.join(BASE_DIR, "..", "barcodes", "src", "run_pdflatex.bat")
    else:
        raise ValueError("Unsupported Operating System")

    script_path = os.path.abspath(script_name)
    print(f"Using script: {script_path}")

    if os_name != "Windows":
        subprocess.run(["chmod", "+x", script_path], check=True)


    subprocess.run(
        [script_path, LATEX_DIR, LOGS],
        check=True,
        capture_output=True,
        text=True
    )

if __name__ == "__main__":
    create_latex()
    create_pdf()
