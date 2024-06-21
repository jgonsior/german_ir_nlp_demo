# Wissenschaftskommunikations Artikel

This repository contains the code and resources used during the Long Night of Science and Technology (LNDW). It includes various scripts, data sets, and other materials created for the event.

## Prerequisites

- Python 3.12.3 (Required for `Wissenschaftskommunikations Artikel/colored barcodes`)

## Installation

To run the code in the `Wissenschaftskommunikations Artikel/colored barcodes` directory, follow these steps to create a virtual environment:

```bash
python3 -m venv <VENV-NAME>
source <VENV-NAME>/bin/activate
pip install -r Wissenschaftskommunikations Artikel/colored barcodes/requirements.txt
```

## Usage

Instructions for executing the code within the `Wissenschaftskommunikations Artikel` directory.

### Colored Barcodes

There are two main files in this section, along with an optional experimental file that might be useful in the future:

- `word2vec.py`
- `generate_colored_barcodes.py`
- `load_embeddings.py` (Optional)

#### `word2vec.py`

This script trains a Word2Vec model, which is then used to generate 27 colored barcode pairs for the `generate_colored_barcodes.py` script. The training data is located at:

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

This function finds the tokens with the highest similarity scores for the given tokens and returns them as tuples in the format `(token: str, similarity score: float)`, where 1.0 is denoted as the highest possible similarity. These pairs are then used in the `generate_colored_barcodes.py` script.

#### `generate_colored_barcodes.py`

This script generates the colored barcodes for comparison. The generated barcodes are saved in `colored barcodes/answers` and `colored barcodes/questions`. The list of matching barcode pairs is defined at the start of the script:

```python
# Has the structure ("question", "answer")
terms_to_display = [
    ("harry", "potter"),
    ("zauberer", "hexen"),
    ("dumbledore", "schulleiter"),
    ("hufflepuff", "branstone"),
    ("tom", "riddle"),
    ("malfoy", "draco"),
    ("bellatrix", "lestrange"),
    ("ariana", "aberforth"),
    ("dolores", "umbridge"),
    ("flitwick", "filius"),
    ("sirius", "severus"),
    ("alexia", "walkin"),
    ("peter", "pettigrew"),
    ("phönixfeder", "kern"),
    ("dobby", "hauself"),
    ("schneeeule", "hedwig"),
    ("lilly", "beschuldigung"),
    ("orden", "phönix"),
    ("adalbert", "schwahfel"),
    ("george", "fred"),
    ("slughorn", "horace"),
    ("heiligtümer", "todes"),
    ("daniel", "radcliffe"),
    ("emma", "watson"),
    ("kammer", "schreckens"),
    ("drachenherzfaser", "weißbuche"),
    ("viktor", "krum"),
]
```

In this list, `"question"` represents the token/barcode used on the question sheets, while `"answer"` represents the barcode generated as the answer.

**IMPORTANT: The index of the question and answer (e.g., `question_0` and `answer_0`) denotes the barcode pair. Ensure that the question and answer pairs have high similarity scores and do not share common similarity scores with other pairs to maintain accurate matching.**
