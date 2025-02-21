# Backend

This folder of the repository contains the code and Setup for the backend using Conda for package management and CUDA for training. It also has installation instructions on the necessary Python versions and environments and deployment of the Flask API.

## Prerequisites

Using [Conda](https://docs.anaconda.com/free/miniconda/) makes it quick and easy to set up packages because it provides precompiled binaries, avoiding manual compilation.
If you want to train install CUDA as well.

-   Required for `./preprocessing`: **Python 3.9.X**
-   Required for `./query_generation/hp_gpl` & for `./RAGatouille`: A Conda Environment, such as: [Miniconda](https://docs.anaconda.com/free/miniconda/) using **Python 3.10.X** and **CUDA** Drivers.

## Installation

To run the code in `./preprocessing` directory, follow these steps to create a virtual environment:

```bash
python3 -m venv <VENV-NAME>
source <VENV-NAME>/bin/activate
pip install -r ./preprocessing/requirements_preprocessing.txt`
```

-   **NOTE:** `python3` should be the PATH to a **Python 3.9.X** Version. Since multiple python versions are required a version management tool could make this process easier, but one could also just type the full path to the required version.

---

To run the code in `./query_generation` directory, follow these steps to create a virtual environment:

```bash
python3.10 m venv <VENV-NAME>
source venv/bin/activate
pip install -r requirements_qgen.txt
```

-   **NOTE:** Python 3.12.X did not work, and working directory should be `./query_generation`

---

<a id="RAGatouille-setup"></a>
To run the code for `./RAGatouille` directory **and to deploy the backend Server/Flask API**, follow these steps to create the **Conda** environment:

**Setup for Training the Model**

```bash
# setup env
conda env create -f RAG_env_conda.yml
conda activate RAG_env_conda
```
## General execution order
```
1. download_wikis.py
2. preprocess_wikis.py
3. process_unicode_characters.py
4. corpus.py
5. querygen.py
6. backend/RAGatouille/data_preprocessing.py
7. backend/scripts/train_index_eval_RAG.sh
8. Deploy Backend Server
```

**! ! ! For further details on what do for this execution order, please read the instructions below. ! ! !**


## 1. Preprocessing

The preprocessing sections contains all the necessary scripts to download and prepare the data for our project.

### Executing `download_wikis.py` (IMPORTANT: To use the `download_wikis.py` file, you must use Python 3.9.X)

1. Add the required URLs to the Fandom Wiki(s) in `WIKI_DUMPS_URLS` (see template)

2. (Optional:) Adjust the `preprocessing_path` Path
3. Execute `python downloads_wikis.py`

**WIKI_DUMPS_URL TEMPLATE**

```py
50    WIKI_DUMPS_URLS = {
51        # https://harrypotter.fandom.com/de/wiki/Spezial:Statistik
52        "harry_potter": "https://s3.amazonaws.com/wikia_xml_dumps/d/de/deharrypotter_pages_current.xml",
53    }
54
55     preprocessing_path = "backend/preprocessing/data"

```

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

## 2. Query Generation - HP GPL

### Required Files

You need the newest preprocessed wiki file:

-   `backend/preprocessing/data/harry_potter_unicode_processed.json`

### Prepare Corpus:

Prepare `corpus.jsonl` like in [data sample](https://github.com/jgonsior/german_ir_nlp_demo/tree/gpl-doc/backend/query_generation/hp_gpl/sample-data).
Execute the `corpus.py` script to create the `corpus.jsonl` from preprocessed wiki JSON file.
Adjust `dir` path for target training data directory

-   **NOTE:** working directory should be `./query_generation/hp_gpl`

### Generate Training Data

Execute `qgen.py` to generate queries and hard negatives, based on the `corpus.jsonl`, to create the `passages.csv`,
and to split the generated data into `train_triples.jsonl`, `eval_triples.jsonl`, and `test_triples.jsonl` sets.
These files are used for the training and evaluation.
Change `generator` and `retrievers` parameters to use different models for query generation and negative mining.
Adjust `data_dir` path for target training data directory.

-   **NOTE:** Other generated files `qgen-qrels/train.tsv`, `data.json`, `hard-negatives.jsonl`, and `qgen-queries.jsonl` are only needed during the creation of the other files. May delete afterwards.

## 3. Training and Evaluation

### Installation

Install the Conda Environment as described [HERE](#RAGatouille-setup), or use `backend/scripts/setup_conda_env.sh` if you only want to train.

-   **NOTE: Make sure that CUDA drivers are installed**

### Data Preprocessing

We used 3 datasets for training. GermanDPR and XQA for understanding german semantics and HP (short for Harry Potter) for learning domain specific Harry Potter terms.

### GermanDPR and XQA Dataset

1. Download and unpack GermanDPR (https://germanquad.s3.amazonaws.com/GermanDPR.zip) and XQA (https://thunlp.s3-us-west-1.amazonaws.com/data_XQA.tar.gz) into `backend/data/qa/GermanDPR` and `backend/data/qa/XQA`.
2. Run `backend/RAGatouille/data_preprocessing.py` to create the files `train_triples.jsonl` and `passages.csv` required for training.

### HP Dataset

1. Generate harry potter related training, evaluation and test queries as described in `backend/query_generation/hp-gpl` and save them in addition to the full Harry Potter Corpus to `backend/data/qa/HP`.

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

All triples files contain on each line a question, one positiive context that answers the question and 3 (GermanDPR, XQA) or 10 (HP) negative contexts:

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

In case of the HP `passages.csv` the `id` can be seperated into `<wiki_page_id> - <passage_position_on_that_page>`, e.g.:

```json
42669-0,"[""Wizarding World] Der Wiesenchampignon (oder Feldegerling), botanisch ""Agaricus campestris"" ist ein großer, weiß-cremefarbener, essbarer Pilz."

has wiki_page_id = 42669
and passage_position_on_that_page = 0
```

### Run Training/Evaluation

Run the training (and evaluation) script`backend/scripts/train_index_eval_RAG.sh` (this is the only script you should modify e.g. if datasets, epochs/partitions or the basemodel differ from our experiments). This will train the base-model (currently `bert-base-german-cased`) on GermanDPR, XQA, HP in this order. After each Dataset the the best checkpoint (from the currently 2 epochs each split into 20 parts) is chosen for further training. To pick the best (=recall@5) checkpoint the HP corpus (`backend/data/qa/HP/passages.csv`) is indexed and the HP evaluation queries (`backend/data/qa/HP/eval_triples.jsonl`) are answered on this index.

### Relevant Python Scripts

-   `backend/RAGatouille/training.py`
-   `backend/RAGatouille/indexing.py`
-   `backend/RAGatouille/evaluate.py`
-   `backend/RAGatouille/add_and_visualize_best_statistics.py` $\rightarrow$ copy the best final checkpoint and add its statistics to `backend/RAGatouille/compare.py`
-   `backend/RAGatouille/compare.py` $\rightarrow$ if you want to directly compare multiple checkpoints

### Results

All checkpoints (one for each partition in each epoch) and their indexes are stored in `backend/data/colbert`. According statistics (recall@k values) are stored in `backend/data/statistics/statistics.csv`.

The best final checkpoint (after all train datasets were applied) is copied along with its index to `backend/data/colbert/best` and its statistics are added to `backend/data/statistics/best_statistics.csv` and visualized in `backend/data/statistics/best_checkpoints.pdf`.

## 4. Flask Endpoints

After deployment the Flask API is accessible under `http://localhost:8080`. Our application defines three key endpoints in `app/main/routes.py`:

1. **/search**

    - **Description**: Returns the best 100 match passages for a given query `q`.
    - **Method**: GET
    - **Parameters**: `q` (query string)
    - **Return Value**: JSON object containing the best match passage.

2. **/document**

    - **Description**: Returns the whole document by the given parameter `id`.
    - **Method**: GET
    - **Parameters**: `id` (document identifier)
    - **Return Value**: JSON object containing the document.

3. **/word_embeddings**
    - **Description**: Returns a score between 0 and 1 for each word to indicate how important the word was in matching the defined query.
    - **Method**: POST
    - **Parameters**: JSON body containing `query` (string) and `paragraph` (string)
    - **Return Value**: JSON object with scores for each word.
