# GPL Query Generation

Steps for GPL Query Generation:

1. prepare 'corpus.jsonl' like in [data sample](sample-data/corpus.jsonl, may use corpus.py script to create from preprocessed wiki json)
2. put 'corpus.jsonl' in folder with arbitrary name
3. cwd should be the project `german_ir_nlp_demo`, then run
    ```bash
    python -m backend.query_generation.querygen
    ```
4. optionally: to split generated into train, eval, and test set uncomment line 138 "format.create_train_eval_test_triples(directory)"

## Fandom Corpus

For now, the corpus data for query generation has to be in jsonl file with passaage, title, and id attribute [data sample](sample-data/corpus.jsonl)
