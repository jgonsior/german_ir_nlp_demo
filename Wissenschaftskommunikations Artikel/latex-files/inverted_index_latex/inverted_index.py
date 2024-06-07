import json
import re
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import spacy

nlp = spacy.load("de_core_news_sm")

# No stemming on these
unprocessed_terms = ['harry potter', 'hogwarts', 'albus dumbledore', 'severus snape', 'voldemort', 'minerva mcgonagall',
                     'potter', 'dumbledore', 'albus', 'minerva', 'mcgonagall', 'snape', 'severus']


def clean_tokens(tokenlist, normalize: bool = True):
    remove_chars = ['"', ',', '.', '[', ']', '{', '}', '(', ')', ':', '-', ';', "'", "!", '“', '„', '&', "''", "'s",
                    '*', '...', '):', '/', '--', '---']
    tokens_filtered = [token.lower() for token in tokenlist if token not in remove_chars]

    stemmer = SnowballStemmer("german")
    stop_words = set(stopwords.words("german"))
    protected_words = set(unprocessed_terms)
    if normalize:
        tokens = []
        for token in tokens_filtered:
            if token in protected_words:
                tokens.append(token)  # Keep protected terms unchanged
            else:
                if token not in stop_words:
                    tokens.append(stemmer.stem(token))
    else:
        tokens = [token for token in tokens_filtered]

    # Filter out unwanted tokens
    filtered_tokens = []
    for token in tokens:
        if token == '10³':
            continue
        if token.isdigit() and (1000 <= int(token) <= 2999):  # Include only valid year numbers
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


def extract_passages(input_text):
    # Use regex to split text by \marginpar{number} to identify sections
    passages = re.split(r'\\marginpar{(\d+)}', input_text)

    # Remove any empty strings resulting from split
    passages = [p for p in passages if p.strip()]

    return passages


def create_inverted_index(files, preprocess=False, normalize=True):
    inverted_index = defaultdict(lambda: defaultdict(list))  # Use set to avoid duplicate entries

    # Regex patterns for ignoring LaTeX commands and text within curly brackets
    ignore_patterns = [
        r'\\[a-zA-Z]+\{[^}]*\}',  # LaTeX commands with arguments
        r'\\[a-zA-Z]+'  # LaTeX commands without arguments
    ]

    # Iterate over the list of files with their indices
    for doc_id, file in enumerate(files, start=1):
        with open(file, 'r', encoding='utf-8') as f:
            input_text = f.read()

        # Extract passages
        passages = extract_passages(input_text)

        # Iterate over the passages with their indices
        for i in range(1, len(passages), 2):
            section_id = int(passages[i])
            text = passages[i + 1]

            # Remove LaTeX commands and text within curly brackets
            for pattern in ignore_patterns:
                text = re.sub(pattern, '', text)

            # Tokenize the text into terms
            terms = re.findall(r'\b\w+\b', text.lower())  # Lowercase terms for consistency

            if preprocess:
                terms = clean_tokens(terms, normalize)

            for term in terms:
                inverted_index[term][doc_id].append(section_id)  # Store as int for easier sorting

    return inverted_index


def abbreviate_sections(sections):
    if not sections:
        return ""

    sections = sorted(sections)
    ranges = []
    range_start = sections[0]
    previous = sections[0]

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

    if range_start == previous:
        ranges.append(f'{range_start}')
    else:
        ranges.append(f'{range_start}-{previous}')

    return ', '.join(ranges)


def generate_latex_table(inverted_index, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write the LaTeX document preamble
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

        # Write the inverted index entries
        for term, doc_dict in sorted(inverted_index.items()):
            doc_entries = []
            for doc_id, sections in doc_dict.items():
                doc_entries.append(rf'\textbf{{Dokument {doc_id}}}: {abbreviate_sections(list(sections))}')
            doc_entry_str = '; '.join(doc_entries)
            f.write(rf'{term} & {doc_entry_str} \\' + '\n')
            f.write(r'\hline' + '\n')

        # Write the LaTeX document end
        f.write(r'\end{longtable}' + '\n')
        f.write(r'\end{document}' + '\n')


def convert_to_regular_dict(d):
    if isinstance(d, defaultdict):
        d = {k: convert_to_regular_dict(v) for k, v in d.items()}
    if isinstance(d, set):
        d = list(d)
    return d


def generate_json_file(files, preprocess=False, normalize=True):
    inverted_index = defaultdict(list)  # Term/Section

    # Regex patterns for ignoring LaTeX commands and text within curly brackets
    ignore_patterns = [
        r'\\[a-zA-Z]+\{[^}]*\}',  # LaTeX commands with arguments
        r'\\[a-zA-Z]+'  # LaTeX commands without arguments
    ]

    # Iterate over the list of files with their indices
    for doc_id, file in enumerate(files, start=1):
        with open(file, 'r', encoding='utf-8') as f:
            input_text = f.read()

        passages = extract_passages(input_text)

        # Iterate over the passages with their indices
        for i in range(1, len(passages), 2):
            section_id = int(passages[i])
            text = passages[i + 1]

            # Remove LaTeX commands and text within curly brackets
            for pattern in ignore_patterns:
                text = re.sub(pattern, '', text)

            terms = re.findall(r'\b\w+\b', text.lower())  # Lowercase terms for consistency
            if preprocess:
                terms = clean_tokens(terms, normalize)
            skip = []
            for term in terms:
                if term not in skip:
                    inverted_index[term].append(str(doc_id) + "-" + str(section_id))
                    skip.append(term)

    # Convert defaultdict to regular dict and lists
    regular_data = convert_to_regular_dict(inverted_index)

    # Generate JSON file
    with open(output_file_json, 'w', encoding='utf-8') as f:
        json.dump(regular_data, f, sort_keys=True, ensure_ascii=False, indent=4)


def main(input_files, output_file_latex, output_file_json, preprocess=False, normalize=True):
    # Create inverted index
    inverted_index = create_inverted_index(input_files, preprocess, normalize)

    # Generate LaTeX table with inverted index
    generate_latex_table(inverted_index, output_file_latex)

    # Generate JSON inverted index
    generate_json_file(input_files, preprocess, normalize)


if __name__ == "__main__":
    input_files = ["src/enumerated/Dumbledore_enumerated.tex", "src/enumerated/HarryPotter_enumerated.tex",
                   "src/enumerated/Hogwarts_enumerated.tex",
                   "src/enumerated/Minerva_enumerated.tex", "src/enumerated/Snape_enumerated.tex",
                   "src/enumerated/Voldemort_enumerated.tex"]
    # Create the inverted index for latex
    output_file_latex = "src/index/inverted_index.tex"

    # Additionally create a json version for further usage
    output_file_json = "src/index/inverted_index.json"

    # Turn off preprocess and normalization manually if needed (unprocessd/processed index)
    preprocess = True
    normalize = True
    main(input_files, output_file_latex, output_file_json, preprocess, normalize)
