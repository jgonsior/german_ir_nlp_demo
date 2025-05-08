import glob
import json
import re
from collections import defaultdict
import os
from pprint import pprint

import spacy
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# Load German language model from spaCy, there could be better models to use, see: https://spacy.io/models/de/
nlp = spacy.load("de_core_news_sm")

# Terms that should not be stemmed to ensure they appear in the inverted index as they are
unprocessed_terms = ['harry potter', 'hogwarts', 'albus dumbledore', 'severus snape', 'voldemort', 'minerva mcgonagall',
                     'potter', 'dumbledore', 'albus', 'minerva', 'mcgonagall', 'snape', 'severus', 'quidditch',
                     'ariana']


# Clean and preprocess tokens from the text, taken from backend code and adapted
def clean_tokens(tokenlist, normalize=True):
    """
    Cleans and preprocesses tokens from the text.

    Args:
    - tokenlist (list): List of tokens to clean and preprocess.
    - normalize (bool): Whether to normalize tokens (default=True).

    Returns:
    - list: Cleaned and processed tokens.
    """
    # Characters to remove from tokens
    remove_chars = ['"', ',', '.', '[', ']', '{', '}', '(', ')', ':', '-', ';', "'", "!", '“', '„', '&', "''", "'s",
                    '*', '...', '):', '/', '--', '---']

    # Filter tokens based on removal characters
    tokens_filtered = [token.lower() for token in tokenlist if token not in remove_chars]

    # Initialize Snowball stemmer for German
    stemmer = SnowballStemmer("german")
    stop_words = set(stopwords.words("german"))

    # Process each token
    tokens = []
    for token in tokens_filtered:
        if token in unprocessed_terms:
            tokens.append(token)  # Keep protected terms unchanged
        else:
            if token not in stop_words:
                tokens.append(stemmer.stem(token)) if normalize else tokens.append(token)

    # Filter out unwanted tokens
    filtered_tokens = []
    for token in tokens:
        if token == '10³':  # Skip specific token
            continue
        if token.isdigit() and (1000 <= int(token) <= 2999):  # Include valid year numbers
            filtered_tokens.append(token)
        if re.match(r'^\d+(\.\d+)?$', token):  # Filter out decimal numbers and numbers with trailing dot
            continue
        if re.match(r'^\d+\.$', token):  # Filter out numbers with trailing dot
            continue
        if len(token) == 1 and not token.isdigit():  # Filter out single letters
            continue
        elif not token.isdigit():  # Include non-numeric tokens
            filtered_tokens.append(token)

    return filtered_tokens


# Extract passages from input text , needed for enumeration later
def extract_passages(input_text):
    """
    Extracts passages from input text based on predefined patterns.

    Args:
    - input_text (str): Input text containing passages.

    Returns:
    - list: List of passages extracted from input text.
    """
    # Split text based on \marginpar{number} to identify sections
    passages = re.split(r'\\marginpar{(\d+)}', input_text)

    # Remove empty strings resulting from split
    passages = [p for p in passages if p.strip()]

    return passages


# Create inverted index from given files
def create_inverted_index(files, preprocess=False, normalize=True):
    """
    Creates an inverted index from a list of files.

    Args:
    - files (list): List of file paths containing text to index.
    - preprocess (bool): Whether to preprocess tokens (default=False).
    - normalize (bool): Whether to normalize tokens (default=True).

    Returns:
    - defaultdict: Inverted index mapping terms to documents and sections.
    """
    inverted_index = defaultdict(lambda: defaultdict(list))

    # Regex patterns for ignoring LaTeX commands and text within curly brackets
    ignore_patterns = [
        r'\\[a-zA-Z]+\{[^}]*\}',  # LaTeX commands with arguments
        r'\\[a-zA-Z]+'  # LaTeX commands without arguments
    ]

    # Iterate over the documents
    for doc_id, file in enumerate(files, start=1):
        with open(file, 'r', encoding='utf-8') as f:
            input_text = f.read()

        # Extract passages from the document
        passages = extract_passages(input_text)

        # Process each passage
        for i in range(1, len(passages), 2):
            section_id = int(passages[i])
            text = passages[i + 1]

            # Track processed terms to avoid duplicates in the inverted index
            section_terms = []

            # Remove LaTeX commands and text within curly brackets
            for pattern in ignore_patterns:
                text = re.sub(pattern, '', text)

            # Tokenize the text into terms
            terms = re.findall(r'\b\w+\b', text.lower())  # Lowercase terms for consistency

            # Clean and preprocess tokens if specified
            if preprocess:
                terms = clean_tokens(terms, normalize)

            # Add terms to the inverted index
            for term in terms:
                if term not in section_terms:
                    inverted_index[term][doc_id].append(section_id)
                    section_terms.append(term)

    return inverted_index


# Abbreviate consecutive section numbers in inverted index (e.g., 111,112,113 -> 111-113)
def abbreviate_sections(sections):
    """
    Abbreviates consecutive section numbers.

    Args:
    - sections (list): List of section numbers to abbreviate.

    Returns:
    - str: Abbreviated section numbers as a string.
    """
    if not sections:
        return ""

    sections = sorted(sections)
    ranges = []
    range_start = sections[0]
    previous = sections[0]

    # Determine consecutive ranges
    for section in sections[1:]:
        if section == previous + 1:
            previous = section
        else:
            if range_start == previous:
                ranges.append(f'{range_start}')
            else:
                ranges.append(f'{range_start}-{previous}')
            range_start = section
            previous = section

    # Add last range
    if range_start == previous:
        ranges.append(f'{range_start}')
    else:
        ranges.append(f'{range_start}-{previous}')

    return ', '.join(ranges)


# Generate LaTeX format for inverted index
def generate_latex_table(inverted_index, output_file):
    """
    Generates a LaTeX table from an inverted index.

    Args:
    - inverted_index (defaultdict): Inverted index mapping terms to documents and sections.
    - output_file (str): Output file path for the LaTeX table.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write LaTeX document preamble
        f.write(r'\documentclass[a5paper]{article}' + '\n')
        f.write(r'\usepackage[a5paper, margin=0.5in]{geometry}' + '\n')
        f.write(r'\usepackage{longtable}' + '\n')
        f.write(r'\usepackage[T1]{fontenc}' + '\n')
        f.write(r'\usepackage[sfdefault]{AlegreyaSans}' + '\n')
        f.write(r'\usepackage{array}' + '\n')
        f.write(r'\usepackage{ragged2e}' + '\n')
        f.write(r'\usepackage[utf8]{inputenc}' + '\n')
        f.write(r'\begin{document}' + '\n')
        f.write(r'\begin{longtable}[l]{|l|p{3in}|}' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\textbf{Term} & \textbf{Dokumenten-ID und Absatz} \\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\endfirsthead' + '\n')

        # Write entries for each term in the inverted index
        for term, doc_dict in sorted(inverted_index.items()):
            doc_entries = []
            for doc_id, sections in doc_dict.items():
                doc_entries.append(rf'\textbf{{Dokument {doc_id}}}: {abbreviate_sections(list(sections))}')
            doc_entry_str = '; '.join(doc_entries)
            f.write(rf'{term} & {doc_entry_str} \\' + '\n')
            f.write(r'\hline' + '\n')

        # Write LaTeX document end
        f.write(r'\end{longtable}' + '\n')
        f.write(r'\end{document}' + '\n')


# Helper function to convert defaultdict to regular dictionary
def convert_to_regular_dict(d):
    """
    Recursively converts a defaultdict to a regular dictionary.

    Args:
    - d (defaultdict): defaultdict to convert.

    Returns:
    - dict: Regular dictionary converted from defaultdict.
    """
    if isinstance(d, defaultdict):
        d = {k: convert_to_regular_dict(v) for k, v in d.items()}
    if isinstance(d, set):
        d = list(d)
    return d


# Generate JSON file from inverted index for barcode generation
def generate_json_file(files, output_file_json, preprocess=False, normalize=True):
    """
    Generates a JSON file from an inverted index.

    Args:
    - files (list): List of file paths containing text to index.
    - output_file_json (str): Output file path for the JSON file.
    - preprocess (bool): Whether to preprocess tokens (default=False).
    - normalize (bool): Whether to normalize tokens (default=True).
    """
    inverted_index = defaultdict(list)  # Term/Section

    # Regex patterns for ignoring LaTeX commands and text within curly brackets
    ignore_patterns = [
        r'\\[a-zA-Z]+\{[^}]*\}',  # LaTeX commands with arguments
        r'\\[a-zA-Z]+'  # LaTeX commands without arguments
    ]

    for doc_id, file in enumerate(files, start=1):
        with open(file, 'r', encoding='utf-8') as f:
            input_text = f.read()

        passages = extract_passages(input_text)

        # Iterate over the passages
        for i in range(1, len(passages), 2):
            section_id = int(passages[i])
            text = passages[i + 1]

            # Remove LaTeX commands and text within curly brackets
            for pattern in ignore_patterns:
                text = re.sub(pattern, '', text)

            terms = re.findall(r'\b\w+\b', text.lower())  # Lowercase terms for consistency
            if preprocess:
                terms = clean_tokens(terms, normalize)

            # Track terms to avoid duplicates in inverted index
            skip = []
            for term in terms:
                if term not in skip:
                    inverted_index[term].append(str(doc_id) + "-" + str(section_id))
                    skip.append(term)

    # Convert defaultdict to regular dictionary and lists
    regular_data = convert_to_regular_dict(inverted_index)

    # Generate JSON file
    with open(output_file_json, 'w', encoding='utf-8') as f:
        json.dump(regular_data, f, sort_keys=True, ensure_ascii=False, indent=4)


# Main function to coordinate indexing and generation
def main(input_files, output_file_latex, output_file_json, preprocess=False, normalize=True):
    """
    Main function to create inverted index, generate LaTeX table, and JSON file.

    Args:
    - input_files (list): List of file paths containing text to index.
    - output_file_latex (str): Output file path for the LaTeX table.
    - output_file_json (str): Output file path for the JSON file.
    - preprocess (bool): Whether to preprocess tokens (default=False).
    - normalize (bool): Whether to normalize tokens (default=True).
    """
    # Create inverted index
    inverted_index = create_inverted_index(input_files, preprocess, normalize)

    # Generate LaTeX table with inverted index
    generate_latex_table(inverted_index, output_file_latex)

    # Generate JSON inverted index for barcodes
    generate_json_file(input_files, output_file_json, preprocess, normalize)


if __name__ == "__main__":
    # Get the base directory of the script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Define input files and output paths
    INPUT_FILES = sorted(glob.glob(os.path.join(BASE_DIR, "..", "docs_latex", "src", "files", "enumerated", "*.tex")))
    OUTPUT_FILE_LATEX = os.path.abspath(os.path.join(BASE_DIR, "src", "index", "inverted_index.tex"))
    OUTPUT_FILE_JSON = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "barcodes", "invIndex", "inverted_index.json"))
    print(f"Input Files: \n {INPUT_FILES}")
    print("LaTeX Output File:", OUTPUT_FILE_LATEX)
    print("JSON Output File:", OUTPUT_FILE_JSON)

    # Run main function with preprocessing and normalization enabled
    preprocess = True
    normalize = True
    main(INPUT_FILES, OUTPUT_FILE_LATEX, OUTPUT_FILE_JSON, preprocess, normalize)
