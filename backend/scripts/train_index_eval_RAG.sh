#!/bin/bash

# Start time
start_time=$(date +%s)

# Epochs variable
epochs="1 2"

# training
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/training.py --pretrained_model_name_or_path bert-base-german-cased --union_train_data GermanDPR --triples_path backend/data/qa/GermanDPR/train_triples.jsonl --corpus_path backend/data/qa/GermanDPR/passages.csv --num_negatives 10 --epochs $epochs --num_parts 20
# indexing
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/indexing.py --train_data GermanDPR-10neg --epochs $epochs --num_parts 20
# evaluate
best_checkpoint_path_German_DPR=$(conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/evaluate.py --train_data GermanDPR-10neg --triples_path backend/data/qa/HP/eval_triples.jsonl --epochs $epochs --num_parts 20 | tail -n 1)

echo "Best checkpoint for GermanDPR: $best_checkpoint_path_German_DPR"

# training
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/training.py --pretrained_model_name_or_path "$best_checkpoint_path_German_DPR" --union_train_data GermanDPR-XQA --triples_path backend/data/qa/XQA/train_triples.jsonl --corpus_path backend/data/qa/XQA/passages.csv --num_negatives 10  --epochs $epochs --num_parts 20
# indexing
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/indexing.py --train_data GermanDPR-XQA-10neg --epochs $epochs --num_parts 20
# evaluate
best_checkpoint_path_XQA=$(conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/evaluate.py --train_data GermanDPR-XQA-10neg --triples_path backend/data/qa/HP/eval_triples.jsonl --epochs $epochs --num_parts 20 | tail -n 1)

echo "Best checkpoint for XQA: $best_checkpoint_path_XQA"

# training
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/training.py --pretrained_model_name_or_path "$best_checkpoint_path_XQA" --union_train_data GermanDPR-XQA-HP --triples_path backend/data/qa/HP/train_triples.jsonl --corpus_path backend/data/qa/HP/passages.csv --num_negatives 10 --epochs $epochs --num_parts 20
# indexing
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/indexing.py --train_data GermanDPR-XQA-HP-10neg --epochs $epochs --num_parts 20
# evaluate
best_checkpoint_path_HP=$(conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/evaluate.py --train_data GermanDPR-XQA-HP-10neg --triples_path backend/data/qa/HP/eval_triples.jsonl --epochs $epochs --num_parts 20 | tail -n 1)

echo "Best checkpoint for HP: $best_checkpoint_path_HP"

# add and visualize best statistics
conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/add_and_visualize_best_statistics.py --best_checkpoint_paths "$best_checkpoint_path_German_DPR" "$best_checkpoint_path_XQA" "$best_checkpoint_path_HP"

# End time
end_time=$(date +%s)
runtime=$((end_time - start_time))
echo "Total execution time: $runtime seconds"
