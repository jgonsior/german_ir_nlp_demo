#!/bin/bash
#SBATCH --time=100:00:00   # walltime
#SBATCH --nodes=1   # number of nodes
#SBATCH --partition=alpha
#SBATCH --gres=gpu:4
#SBATCH --ntasks=1      # limit to one node
#SBATCH --cpus-per-task=16  # number of processor cores (i.e. threads)
#SBATCH --mem=128G
#SBATCH --mail-user=florian_maurus.mueller@mailbox.tu-dresden.de   # email address
#SBATCH --mail-type=FAIL
#SBATCH -J tie_RAG

# training
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/training.py --pretrained_model_name_or_path bert-base-german-cased --union_train_data GermanDPR --triples_path backend/data/qa/GermanDPR/train_triples.jsonl --corpus_path backend/data/qa/GermanDPR/passages.csv --num_negatives 10 --epochs 1 2 --num_parts 20
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/training.py --pretrained_model_name_or_path backend/data/colbert/checkpoints/bert-base-german-cased/GermanDPR-10neg/epoch1/part10 --union_train_data GermanDPR-XQA --triples_path backend/data/qa/XQA/train_triples.jsonl --corpus_path backend/data/qa/XQA/passages.csv --num_negatives 10  --epochs 1 2 --num_parts 20
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/training.py --pretrained_model_name_or_path backend/data/colbert/checkpoints/bert-base-german-cased/GermanDPR-XQA-10neg/epoch1/part20 --union_train_data GermanDPR-XQA-HP --triples_path backend/data/qa/HP/train_triples.jsonl --corpus_path backend/data/qa/HP/passages.csv --num_negatives 10 --epochs 1 2 --num_parts 20

# indexing
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/indexing.py --train_data GermanDPR-10neg --epochs 1 2 --parts 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/indexing.py --train_data GermanDPR-XQA-10neg --epochs 1 2 --parts 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/indexing.py --train_data GermanDPR-XQA-HP-10neg --epochs 1 2 --parts 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

# evaluate
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/evaluate.py --train_data GermanDPR-10neg --triples_path backend/data/qa/HP/eval_triples.jsonl --epochs 1 2 --parts 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/evaluate.py --train_data GermanDPR-XQA-10neg --triples_path backend/data/qa/HP/eval_triples.jsonl --epochs 1 2 --parts 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/evaluate.py --train_data GermanDPR-XQA-HP-10neg --triples_path backend/data/qa/HP/eval_triples.jsonl --epochs 1 2 --parts 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
