# Backend

## Deploy Backend Server

Install Conda Environment: [Miniconda](https://docs.anaconda.com/free/miniconda/)

```python
# setup env
conda env create -f RAG_env_conda.yml
conda activate RAG_env_conda

# deploy
python run.py
```

Die Flask API ist nun unter `localhost:8080` erreichbar und erwartet eine GET-Anfrage an dem Endpunkt `/search`

**Beispiel**

```python
http://localhost:8080/search?q=Wer hat Snape ermordet?
```

## Training and Evaluation

### Installation

Install the Conda Environment as described above or use `backend/scripts/setup_conda_env.sh` if you only want to train.
Install CUDA.

### Data Preprocessing

We used 3 datasets for training. GermanDPR and XQA for understanding german semantics and HP (short for Harry Potter) for learning domain specific Harry Potter terms.

### GermanDPR and XQA Dataset

1. Download and unpack GermanDPR (https://germanquad.s3.amazonaws.com/GermanDPR.zip) and XQA (https://thunlp.s3-us-west-1.amazonaws.com/data_XQA.tar.gz) into `backend/data/qa/GermanDPR` and `backend/data/qa/XQA`.
2. Run `backend/RAGatouille/data_preprocessing.py` to create the files `train_triples.jsonl` and `passages.csv` required for training.

### HP Dataset

1. Generate harry potter related training, evaluation and test queries as described in `backend/query_generation` TODO and save them in addition to the full Harry Potter Corpus to `backend/data/qa/HP`.

### Required Files

You should now have the following files:

-   `backend/data/qa/GermanDPR/train_triples.jsonl`
-   `backend/data/qa/GermanDPR/passages.csv`
-   `backend/data/qa/XQA/train_triples.jsonl`
-   `backend/data/qa/XQA/passages.csv`
-   `backend/data/qa/HP/train_triples.jsonl`
-   `backend/data/qa/HP/eval_triples.jsonl`
-   `backend/data/qa/HP/test_triples.jsonl`
-   `backend/data/qa/HP/passages.csv`

All triples files contain on each line a question, one positive context that answers the question and 3 (GermanDPR, XQA) or 10 (HP) negative contexts:

```json
{
	"question": "Wie viele christlichen Menschen in Deutschland glauben an einen Gott?",
	"positive_contexts": [
		"Gott\\n\\n=== Demografie ===\\nEine Zusammenfassung von ... als in Ostdeutschland (26 %)."
	],
	"negative_contexts": [
		"Christentum\\n\\n=== Ursprung und Einflüsse ===\\nDie ersten Christen waren ... Jahr des Herrn.",
		"Noachidische_Gebote\\n\\n=== Die kommende Welt ===\\nDer Glaube ... Gute entscheiden.",
		"Figuren_und_Schauplätze_der_Scheibenwelt-Romane ... einen Gott damit entmachten."
	]
}
```

All passage files are of the form:

```json
id,passage_text
42669-0,"[""Wizarding World] Der Wiesenchampignon (oder Feldegerling), botanisch ""Agaricus campestris"" ist ein großer, weiß-cremefarbener, essbarer Pilz."
42669-1,"[Geschichte] Lyall Lupin gewann die Zuneigung ... den Irrwicht, der Hope Howell ängstigte, in einen Wiesenchampignon zu verwandeln."
```

In case of the HP `passages.csv` the `id` can be seperated into `wiki_page_id - passage_position_on_that_page`.

### Run Training/Evaluation

Run the training (and evaluation) script`backend/scripts/train_index_eval_RAG.sh` (this is the only script you should modify e.g. if datasets, epochs/partitions or the basemodel differ from our experiments). This will train the base-model (currently `bert-base-german-cased`) on GermanDPR, XQA, HP in this order. After each Dataset the the best checkpoint (from the currently 2 epochs each split into 20 parts) is chosen for further training. To pick the best (=recall@5) checkpoint the HP corpus (`backend/data/qa/HP/passages.csv`) is indexed and the HP evaluation queries (`backend/data/qa/HP/eval_triples.jsonl`) are answered on this index.

### Relevant Python Scripts

-   `backend/RAGatouille/training.py`
-   `backend/RAGatouille/indexing.py`
-   `backend/RAGatouille/evaluate.py`
-   `backend/RAGatouille/add_and_visualize_best_statistics.py` // copy best final checkpoint and add its statistics to `backend/RAGatouille/compare.py`
-   `backend/RAGatouille/compare.py` // if you want to directly compare multiple checkpoints

### Results

All checkpoints (one for each partition in each epoch) and their indexes are stored in `backend/data/colbert`. According statistics (recall@k values) are stored in `backend/data/statistics/statistics.csv`.

The best final checkpoint (after all train datasets were applied) is copied along with its index to `backend/data/colbert/best` and its statistics are added to `backend/data/statistics/best_statistics.csv` and visualized in `backend/data/statistics/best_checkpoints.pdf`.

## Preprocessing

### Installing dependencies

```python
python -m venv venv
source venv/bin/activate
pip install -r requirements_preprocessing.txt
```

### Executing `download_wikis.py` (IMPORTANT: To use the `download_wikis.py` file, you must use Python 3.9.X)

1. Add the required URLs to the Fandom Wiki(s) in `WIKI_DUMPS_URLS` (see template)

2. (Optional:) Adjust the `preprocessing_path` Path
3. Execute `python downloads_wikis.py`

### Executing `preprocess_wikis.py`

1. Adjust `WIKI_PATHS` to point to the correct directory that contains the `dumps/` files from `downloads_wikis.py`
2. Execute `python preprocess_wikis.py`

```python
def split_page_in_paragraphs(wiki_page, max_heading_length=5, max_words_per_parag=250, min_words_per_parag=1, regex=None):
    parags = wiki_page.split("\n")

    # first iteration: drop links and empty lines
    clean_parags = []
    for parag in parags:
        parag = parag.strip()

        # Remove "}}" or "{{" and all characters up to the next space
        parag = re.sub(r"(\}\}|\{\{)[^ ]*", "", parag)

        # Remove unnecessary patterns and characters
        parag = re.sub(r"&amp;", "&", parag)
        parag = re.sub(r"\[ b\]", "", parag)
        parag = re.sub(r"\[src\]", "", parag)

        parag = re.sub(SPECIFIC_TEXT, "", parag)
        parag = re.sub(r"\"&lt;/ref&gt;", "", parag)

        if regex is not None and regex.match(parag):
            continue

        if parag == "":
            continue

        clean_parags.append(parag)

    ...
```

In this code sample the filtering of unwanted text structures (like html artifacts and such) are filtered out. It might be possible that there are still some artifacts which can be found in the texts, so adjustments can be made here.

### (Optional) Removing Unicode characters

This file serves to remove the remaining unicode artifcats that are not properly changed while loading and storing the json file. It is especially useful for letters such as "ö, ä, ß, ü" etc. It might be possible that there are still fragments which could be found,
though these are usually just empty space symbols.

1. Adjust the `file_path` to point to the preprocessed `.json` file.
2. Execute `python process_unicode_characters.py`

## Query Generation - HP GPL

### Installing dependencies

```python
python3.10 m venv venv
source venv/bin/activate
pip install -r requirements_qgen.txt
```

Note: Python 3.12.X did not work

### Required Files

You need following file:

-   `backend/preprocessing/data/harry_potter_unicode_processed.json`

### Prepare Corpus:

Prepare `corpus.jsonl` like in [data sample](URL)
You may use the `corpus.py` script to create corpus.jsonl from preprocessed wiki JSON file.
Adjust `dir` path for target training data directory

### Generate Training Data

Execute `qgen.py` to generate queries and hard negatives, based on the `corpus.jsonl`, to create the `passages.csv`,
and to split the generated data into `train_triples.jsonl`, `eval_triples.jsonl`, and `test_triples.jsonl` sets.
These files are used for the training and evaluation.
Change `generator` and `retrievers` parameters to use different models for query generation and hard negatives.

Note: Other generated files `qgen-qrels/train.tsv`, `hard-negatives.jsonl` are only needed during the creation of the other files. May delete afterwards.
