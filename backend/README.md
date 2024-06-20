### Deploy Backend Server

Install Conda Environment:  [Miniconda](https://docs.anaconda.com/free/miniconda/)

```
# setup env
conda env create -f RAG_env_conda.yml
conda activate RAG_env_conda

# deploy
python run.py
```

Die Flask API ist nun unter `localhost:8080` erreichbar und erwartet eine GET-Anfrage an dem Endpunkt `/search`

**Beispiel**
```
http://localhost:8080/search?q=Wer hat Snape ermordet?
```

# Training and Evaluation

## Installation
Install the Conda Environment as described above or use `backend/scripts/setup_conda_env.sh` if you only want to train.
Install CUDA.


## Data Preprocessing

We used 3 datasets for training. GermanDPR and XQA for understanding german semantics and HP (short for Harry Potter) for learning domain specific Harry Potter terms.

### GermanDPR and XQA Dataset
1. Download and unpack GermanDPR (https://germanquad.s3.amazonaws.com/GermanDPR.zip) and XQA (https://thunlp.s3-us-west-1.amazonaws.com/data_XQA.tar.gz) into `backend/data/qa/GermanDPR` and `backend/data/qa/XQA`.
2. Run `backend/RAGatouille/data_preprocessing.py` to create the files `train_triples.jsonl` and `passages.csv` required for training.

### HP Dataset
1. Generate harry potter related training, evaluation and test queries as described in `backend/query_generation` TODO and save them in addition to the full Harry Potter Corpus to `backend/data/qa/HP`.

### Required Files
You should now have the following files:
- `backend/data/qa/GermanDPR/train_triples.jsonl`
- `backend/data/qa/GermanDPR/passages.csv`
- `backend/data/qa/XQA/train_triples.jsonl`
- `backend/data/qa/XQA/passages.csv`
- `backend/data/qa/HP/train_triples.jsonl`
- `backend/data/qa/HP/eval_triples.jsonl`
- `backend/data/qa/HP/test_triples.jsonl`
- `backend/data/qa/HP/passages.csv`

All triples files contain on each line a question, one positiive context that answers the question and 3 (GermanDPR, XQA) or 10 (HP) negative contexts:
```
{
    "question":"Wie viele christlichen Menschen in Deutschland glauben an einen Gott?",
    "positive_contexts":[
        "Gott\\n\\n=== Demografie ===\\nEine Zusammenfassung von ... als in Ostdeutschland (26 %)."
    ],
    "negative_contexts":[
        "Christentum\\n\\n=== Ursprung und Einflüsse ===\\nDie ersten Christen waren ... Jahr des Herrn.",
        "Noachidische_Gebote\\n\\n=== Die kommende Welt ===\\nDer Glaube ... Gute entscheiden.",
        "Figuren_und_Schauplätze_der_Scheibenwelt-Romane ... einen Gott damit entmachten."
    ]
}
```

All passage files are of the form:
```
id,passage_text
42669-0,"[""Wizarding World] Der Wiesenchampignon (oder Feldegerling), botanisch ""Agaricus campestris"" ist ein großer, weiß-cremefarbener, essbarer Pilz."
42669-1,"[Geschichte] Lyall Lupin gewann die Zuneigung ... den Irrwicht, der Hope Howell ängstigte, in einen Wiesenchampignon zu verwandeln."
```
In case of the HP `passages.csv` the `id` can be seperated into `wiki_page_id - passage_position_on_that_page`.

## Run Training/Evaluation
Run the training (and evaluation) script`backend/scripts/train_index_eval_RAG.sh` (this is the only script you should modify e.g. if datasets, epochs/partitions or the basemodel differ from our experiments). This will train the base-model (currently `bert-base-german-cased`) on GermanDPR, XQA, HP in this order. After each Dataset the the best checkpoint (from the currently 2 epochs each split into 20 parts) is chosen for further training. To pick the best (=recall@5) checkpoint the HP corpus (`backend/data/qa/HP/passages.csv`) is indexed and the HP evaluation queries (`backend/data/qa/HP/eval_triples.jsonl`) are answered on this index.

### Relevant Python Scripts
- `backend/RAGatouille/training.py`
- `backend/RAGatouille/indexing.py`
- `backend/RAGatouille/evaluate.py`
- `backend/RAGatouille/add_and_visualize_best_statistics.py` // copy best final checkpoint and add its statistics to `backend/RAGatouille/compare.py`
- `backend/RAGatouille/compare.py` // if you want to directly compare multiple checkpoints

## Results
All checkpoints (one for each partition in each epoch) and their indexes are stored in `backend/data/colbert`. According statistics (recall@k values) are stored in `backend/data/statistics/statistics.csv`. 

The best final checkpoint (after all train datasets were applied) is copied along with its index to `backend/data/colbert/best` and its statistics are added to `backend/data/statistics/best_statistics.csv` and visualized in `backend/data/statistics/best_checkpoints.pdf`.





