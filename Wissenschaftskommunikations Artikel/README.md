# Wissenschaftskommunikations Artikel

This repository contains the code and resources used during the Long Night of Science and Technology (LNDW). It includes
various scripts, data sets, and other materials created for the event.

## Prerequisites

- Required for `./colored barcodes` , `./latex-files` and `./sliding-window`: **Python 3.12.3**
- Required for generating LaTeX files: [Inkscape](https://inkscape.org/) & **LaTeX**, such
  as: [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/)
    - _Note: ensure that `pdflatex` and `xelatex` can be executed from the terminal, check your `$PATH` configuration if
      it can't be found_

## Installation

To run the code in the `./colored barcodes`, `./latex-files` and `./sliding-window` directory, follow these steps to create a virtual
environment:

```bash
python3 -m venv <VENV-NAME>
source <VENV-NAME>/bin/activate
pip install -r Wissenschaftskommunikations Artikel/requirements.txt
```

## Usage

Instructions for executing the code within the `Wissenschaftskommunikations Artikel` directory.

### Latex Representations

Documents, Inverted Index and Query Cards are represented as LateX files. First the Documents have to be generated with
its desired
content and format. Later on the section will be enumerated
to display the section number inside the documents, next to the current section.
Once the documents are generated and enumerated, the next step is to create an inverted index in LaTeX. The inverted
index will be presented as a LaTeX
table that maps each term to the documents and sections in which it appears.

The query cards will be also automatically generated, after the barcode and embedding generation.

#### Manual Processing

Before actual processing of the documents, some manual adjustments and processing has to be done, which hasnt been
automated so far.
This includes:

- Getting the actual text from the wiki and storing it somewhere (raw)
- Formatting the documents by adding desired spaces between sections
- Setting up the desired latex header format

The header for the documents used is structured like this:

``` latex
\documentclass[a4paper, 10pt]{article}
\usepackage{graphicx}
\usepackage[T1]{fontenc}
\usepackage[sfdefault]{AlegreyaSans} %% Option 'black' gives heavier bold face
\usepackage[a4paper, left=2cm, right=2cm, bottom=2cm, top=2cm, marginparsep=0.3in]{geometry} % Adjust left and right margins
\usepackage{amsmath} % for \boxed
\usepackage{fontspec}
\usepackage{sectsty}

\setmainfont{ParryHotter.ttf}

% Setting section fonts
\sectionfont{\fontspec{ParryHotter.ttf}\selectfont}
\subsectionfont{\fontspec{parambol.ttf}\selectfont}
\subsubsectionfont{\fontspec{parambol.ttf}\selectfont}

\setlength{\fboxrule}{2pt}

\begin{document}

\begin{minipage}[t]{\textwidth}
    \vspace*{-1.5cm}
    \begin{flushright}
        \hspace*{\fill}
        \includegraphics[width=4cm]{1.png} % Image of id_images inserted here
    \end{flushright}
\end{minipage}

\section*{\huge Title}

%************** DOCUMENT TEXT **************

\end{document}
\end{document}
```

The text from the desired document then has to be inserted by manually pasting it the into indicated area inside the
latex document.
Formatting of sections is done by using the combination of `\vspace{10pt}` and `\newline` after each section.
(Sub)sections have also been defined manually in the document and require proper formatting.

Special cases like lists, quotes or similar require some individual formatting, to look well formatted in the result.
Individual font sizes have to be set for certain sections, depending on font type or header type, to
fit the overall look.

Some Excerpt of a sample document:

``` latex
\subsubsection*{\large Nach dem Tode} 
„Albus Severus Potter, du bist nach zwei Schulleitern von Hogwarts benannt. Einer von ihnen war in Slytherin und er war wahrscheinlich der mutigste Mann, den ich je kannte. “
\vspace{10pt}
\newline 
— Harry Potter zu seinem Sohn über Severus Snape
\vspace{10pt}
\newline
(Engl.  Albus Severus Potter, you were named after two headmasters of Hogwarts. One of them was a Slytherin and he was the bravest man I ever knew. )
\vspace{10pt}
\newline
Neunzehn Jahre nach dem Sieg über Lord Voldemort machte sich der jüngere von Harry Potters Söhnen, der den Namen Albus Severus, trägt, Sorgen darüber, dass er statt für Gryffindor vielleicht für Slytherin ausgewählt würde. Darauf erklärte ihm Harry, dass Albus Severus nach einem sehr mutigen Schulleiter aus Slytherin benannt wurde.
```

Due to the manual processing, resulting documents may vary regarding number of sections. Thus, the inverted
index and resulting barcodes depend on the latex document sections and are independent from backend implementations.

#### Enumeration

In order to detect the corresponding section inside the latex documents, they have to be enumerated . The enumeration
processed has been partially automated.

#### `doc_enumerator.py`

This script enumerates the documents meaning it adds the number of the section next to the
section in the LateX Document.

The process involves three steps:

- Provided the documents to be enumerated
- Insertion of `%ABSATZ` Comments
- Manual adjustments
- Replacement with `\marginpar{}` commands

The generated LateX documents have to be provided inside the `latex-files/docs_latex/src/files/raw` folder.
The script will load all documents, which are inside this folder automatically.

The script first scans through the LaTeX document and adds a `%ABSATZ` comment after every `\newline` command because it
will most likely represent a section.
The `%ABSATZ` comments serve as placeholders, allowing for manual adjustments.
Users have to add or remove `%ABSATZ` comments because the automatic detection is not sufficient.
Those can easily be detected by eye.

After the %ABSATZ comments are added, the script replaces each generated and manually added `%ABSATZ` comment with
a `\marginpar{section number}` command. This command places the section number in the margin next to the corresponding
section of the text.
All comments will lateron be replaced by the LatEx command `\marginpar{>section number<}`.

All files will be saved in a specific folder in `latex-files/docs_latex/src/files/enumerated`. This folder will lateron
be used by the inverted index.

Result should look like this e.g. compared to before

``` latex
\subsubsection*{\large Nach dem Tode}
\marginpar{16} 
„Albus Severus Potter, du bist nach zwei Schulleitern von Hogwarts benannt. Einer von ihnen war in Slytherin und er war wahrscheinlich der mutigste Mann, den ich je kannte. “
\vspace{10pt}
\newline
\marginpar{17}  
— Harry Potter zu seinem Sohn über Severus Snape
\vspace{10pt}
\newline
\marginpar{18}  
(  Engl.  Albus Severus Potter, you were named after two headmasters of Hogwarts. One of them was a Slytherin and he was the bravest man I ever knew. )
\vspace{10pt}
\newline
\marginpar{19}  
Neunzehn Jahre nach dem Sieg über Lord Voldemort machte sich der jüngere von Harry Potters Söhnen, der den Namen Albus Severus, trägt, Sorgen darüber, dass er statt für Gryffindor vielleicht für Slytherin ausgewählt würde. Darauf erklärte ihm Harry, dass Albus Severus nach einem sehr mutigen Schulleiter aus Slytherin benannt wurde.
```

#### Inverted Index

The inverted index for the latex documents is generated in:

#### `inverted_index.py`

All previously generated documents from `latex-files/docs_latex/src/files/enumerated` will be used to create an inverted
index
on that documents. It uses NLP techniques to clean and preprocess the text, and it outputs the index in both LaTeX and
JSON formats. 
This involves several steps:

- preprocessing  and cleaning the text (can be turned off)
- generate the inverted index
- generate a LateX table for it
- generate a JSON Structure for it (separately)

**Important: If preprocessing is turned off, this part will be skipped.**
Terms are cleaned and processed, filtering out specific number ranges, single letters, and floating-point numbers.
A list of protected terms prevents essential keywords from being stemmed.


Within `create_inverted_index()` the actual inverted index is created. It extracts each sections inside the document ("
passages") with
`extract_passages()` and iterates over its content, extracting the terms of the current section. Duplicates are
discarded.

The actual LateX table is constructed inside `generate_latex_table()`. The LaTeX table is constructed with a predefined
header and populated with index data.
Consecutive section numbers are abbreviated for brevity. The final LateX file will be saved
to `latex-files/inverted_index_latex/index` as `inverted_index.tex`. This file can then be compiled inside LateX
manually.

Finally, the Json File will be generated inside `generate_json_file()` , which will saved inside `barcodes/invIndex`, to
be used for the barcode generation lateron.

``` json
{
    "13e": [
        "1-46"
    ],
    "1792": [
        "1-107"
    ],
    "1874": [
        "1-319"
    ],
    "1881": [
        "1-1",
        "1-6",
        "1-7"
    ],
    "1892": [
        "1-6",
        "1-10"
    ],
    
    ......
```

#### Query Card Generation

The query cards are generated inside:

`query_card_generator.py`

It requires a txt file located inside `queries_latex/res` called `queries.txt`, which should have the following layout:

```
Wie ist Ariana Dumbledore verstorben? #schwer #SPOILER
Wer ist Dumbledore? #leicht
Welche ungewöhnliche Aktivität hat Dumbledore nach seiner Ernennung als Schulleiter von Hogwarts begonnen? #schwer
Wo wurde Dumbledore begraben? #mittel #SPOILER
Wer ist Harry Potter? #leicht
```

The input file (input.txt) should contain queries, each on a new line. Tags indicating difficulty and spoilers are
specified using hashtags (#):

The script generates a LaTeX document (output.tex) with the following structure for each query card:

- Barcode
- Question text
- Embedding
- Image based on difficulty and spoiler tags

Images and SVG files must be provided in the LaTeX document manually. No loading of image files happens automatically.

The output file is a LaTeX file located at latex-files/queries_latex/out/queries.txt and generates multiple A5 pages. To
facilitate merging the A5 pages into A4 format for double-sided printing, the document is structured as follows:

Two question cards (each with a corresponding barcode and embedding) are generated.
Followed by two images based on difficulty and spoiler warnings.
Each set of four A5 pages represents one A4 document, ready for double-sided printing.

Merging of the pdfs from 2x A5 to A4 has to be done manually.

### Colored Barcodes

There are two main files in this section, along with an optional experimental file that might be useful in the future:

- `word2vec.py`
- `generate_colored_barcodes.py`
- `load_embeddings.py` (Optional)

#### `word2vec.py`

This script trains a Word2Vec model, which is then used to generate 27 colored barcode pairs for
the `generate_colored_barcodes.py` script. The training data is located at:

- `backend/preprocessing/data/harry_potter_unicode_processed.json`

Once the model is trained, you can find the most similar terms using the following function:

```python
def find_most_similar(model: Word2Vec, tokens: list[str]) -> None:
    """
    Find and print the most similar terms for each token in the given list.

    Args:
        model (Word2Vec): The trained Word2Vec model.
        tokens (list[str]): A list of tokens for which to find similar terms.
    """
    for token in tokens:
        print(f"Most similar terms for the token {token}: \n {model.wv.most_similar(token.lower())}")
```

This function finds the tokens with the highest similarity scores for the given tokens and returns them as tuples in the
format `(token: str, similarity score: float)`, where 1.0 is denoted as the highest possible similarity. These pairs are
then used in the `generate_colored_barcodes.py` script.

#### `generate_colored_barcodes.py`

This script generates colored barcodes for comparison. The generated barcodes are saved in `colored barcodes/answers`
and `colored barcodes/questions`. The list of matching barcode pairs is defined at the start of the script:

```python
# Has the structure ("question", "answer", "answer_<DOC_ID-PASSAGE_ID>")

terms_to_display = [
    ("harry", "potter", "1-221"),
    ("zauberer", "hexen", "1-1"),
    ("dumbledore", "schulleiter", "1-46"),
    ("hufflepuff", "branstone", "1-144"),
    ("tom", "riddle", "2-1"),
    ("malfoy", "draco", "2-68"),
    ("bellatrix", "lestrange", "2-55"),
    ("ariana", "aberforth", "2-59"),
    ("dolores", "umbridge", "2-73"),
    ("flitwick", "filius", "6-1"),
    ("sirius", "severus", "6-2"),
    ("alexia", "walkin", "6-77"),
    ("peter", "pettigrew", "6-78"),
    ("phönixfeder", "kern", "4-2"),
    ("dobby", "hauself", "4-69"),
    ("schneeeule", "hedwig", "4-8"),
    ("lilly", "beschuldigung", "4-60"),
    ("orden", "phönix", "4-78"),
    ("adalbert", "schwahfel", "4-13"),
    ("george", "fred", "5-1"),
    ("slughorn", "horace", "5-20"),
    ("heiligtümer", "todes", "3-1"),
    ("daniel", "radcliffe", "3-117"),
    ("emma", "watson", "3-12"),
    ("kammer", "schreckens", "3-24"),
    ("drachenherzfaser", "weißbuche", "3-2"),
    ("viktor", "krum", "3-200"),
]

```

In this list, `"question"` represents the token/barcode used on the question sheets, while `"answer"` represents the
barcode generated as the answer.

**IMPORTANT:** The index of the question and answer (e.g., `question_0` and `answer_<DOC_ID-PASSAGE_ID>`) denotes the
barcode pair. Ensure that the question and answer pairs have high similarity scores and do not share common similarity
scores with other pairs to maintain accurate matching, as well as denoting the passage where the solution can be found
as it is essential for the creation of LaTeX files.

#### generate_solution_tex.py

This script generates the solution A4 sheet for the colored barcodes. The solution file can be found in:

- `Wissenschaftskommunikations Artikel/colored barcodes/generated barcodes/latex logs/documents_colored.pdf`

The following function, as the name suggests, creates the LaTeX file which will be used to generate the A4 PDF file for
the solution sheets.

```py
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

```

Within the `create_latex()` function,
the `Wissenschaftskommunikations Artikel/barcodes/template/documents_colored_stub.tex` template gets called. This
template has the following structure:

```latex
% Wissenschaftskommunikations Artikel/barcodes/template/documents_colored_stub.tex

\documentclass[a4paper, 10pt]{article}
\usepackage{graphicx}
\usepackage[inkscapepath=Wissenschaftskommunikations Artikel/colored barcodes/answers/inkscape_out/]{svg}
\usepackage[a4paper, left=0.5cm, right=0.5cm, top=0.5cm, bottom=0.5cm]{geometry}
\usepackage{amsmath} % for \boxed

\svgpath{{Wissenschaftskommunikations Artikel/colored barcodes/answers/}}
\setlength{\fboxrule}{2pt}

\begin{document}
    \thispagestyle{empty}
    \BLOCK{ for document in lst_files }
    \BLOCK{ set document_name = document.split("_")[1] }
    \begin{minipage}[t]{0.15\textwidth}
        \BLOCK{ set decl = document_name|length }
        \vspace*{-3.5cm}
        # if decl == 3
        \hspace*{1.25cm}
        # elif decl == 4
        \hspace*{0.75cm}
        # else
        \hspace*{0.25cm}
        # endif
        $\boxed{\textbf{\Huge\VAR{ document_name }}}$
    \end{minipage}
    \begin{minipage}[t]{0.85\textwidth}
        \includesvg[scale=0.45]{\VAR{ document }}
    \end{minipage}

    # if loop.index % 17 == 0
    \thispagestyle{empty}
    # endif
    \BLOCK{ endfor }
\end{document}
```

This LaTeX file will be used for the [Jinja2](https://github.com/pallets/jinja) environment, which is capable of
generating LaTeX files using Python code. \
In short, Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing
code similar to Python syntax. Then the template is passed data to render the final document. For future information of
usage, please visit their documentation.

Though, the most important lines which might need adjustment are:

```latex
% Wissenschaftskommunikations Artikel/barcodes/template/documents_colored_stub.tex
\BLOCK{ set decl = document_name|length }
\vspace*{-3.5cm}
# if decl == 3
\hspace*{1.25cm}
# elif decl == 4
\hspace*{0.75cm}
# else
\hspace*{0.25cm}
# endif
$\boxed{\textbf{\Huge\VAR{ document_name }}}$
```

Here, the `\vspace` and `\hspace` are used to properly place the numbering of the solutions passages. In case there is
slight misalignment, these values should be adjusted.

```latex
% Wissenschaftskommunikations Artikel/barcodes/template/documents_colored_stub.tex
\includesvg[scale=0.45]{\VAR{ document }}
```

The scale factor is used to get the barcodes properly onto the page, the number 0.45 represents a scaling of 45%
compared to the original scaling.

### Sliding Window

#### `sliding_window_cutting_template.pptx`

The sliding window aka "Masked Language Model" is the part the computer learns context of words. So instead of looking
at a single word individually, the computer will get to know other words that are closely connected to the target word.
In this example it is two words before the target word and two words after. This is a static file (not generated or used
in any algorithms) to be adjusted manually only if any changes to `BOX_WIDTH` or `BOX_SPACING` in `run_generator.py`
were made. If you do not plan to change this, there is a ready-to-print version already for you in `output` directory.
It contains some instructions in German what parts to cut with a cutter blade even though that should be pretty much
self-explanatory.

#### `source-material/selected-passages.json`

Contains only the text passages from our documents that are to be printed. The format is chosen so that existing
structured information such as `Wissenschaftskommunikations Artikel/text passages/harry_potter.json` can be easily added
and scaled for thousands of documents if needed. The existing 3 text passages were added manually.

If you plan to add more text passages make sure that individual words should have more than 18 characters. Otherwise you
will need to adjust some parameters or even the cutting template. It is highly recommended to manually select text
passages that fit best within a regular A4 page. Keep in mind that you will probably not need more than 2 or 3 different
examples for people to get your "scientific idea" you want to explain.

The file needs to have this format - the "id" is optional but helps to connect the previous processes and steps:

```json
[
  {
    "id": "DOC ID",
    "text": [
      "TEXT 1",
      "TEXT 2",
      "TEXT 3"
    ]
  },
  {
    "id": "DOC ID",
    "text": [
      "TEXT 1",
      "TEXT 2",
      "TEXT 3"
    ]
  },
  ...
]
```

#### `run_generator.py`

The only file you need to execute for this part. It will Iterate over the latex templates and create two files for every
text passage in `source-material/selected-passages.json`. One part contains every word in a single box that is to be
used with the `sliding_window_cutting_template.pptx`. The other part contains the result after every word and the
corresponding context has been read.

#### `output`

If you do not plan to change any values or parameters, you can print all files within the `output` directory.
