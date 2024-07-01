from beir.datasets.data_loader import GenericDataLoader
from gpl.toolkit import (
    qgen,
    NegativeMiner,
    PseudoLabeler,
     set_logger_format,
)
import os
import logging
import format_json as format
from typing import List


set_logger_format()
logger = logging.getLogger()  


def querygen_gpl(
    path_to_generated_data: str,
    qgen_prefix: str = "qgen",
    generator: str = "BeIR/query-gen-msmarco-t5-base-v1",
    batch_size_generation: int = 32,
    queries_per_passage: int = 3,

    batch_size_gpl: int = 32,
    max_seq_length: int = 350,
    gpl_steps: int = 140000,
    cross_encoder: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",

    retrievers: List[str] = ["msmarco-distilbert-base-v3", "msmarco-MiniLM-L-6-v3"],
    retriever_score_functions: List[str] = ["cos_sim", "cos_sim"],
    negatives_per_query: int = 10,
):

    #### Make sure there is a `corpus.jsonl` file. It should be under either `path_to_generated_data` ####
    os.makedirs(path_to_generated_data, exist_ok=True)
    assert "corpus.jsonl" in os.listdir(path_to_generated_data
        ), "Corpus should exist!"
    corpus = GenericDataLoader(path_to_generated_data).load_corpus()        

    #### Adjust the QQP automatically, if needed ####
    if queries_per_passage == -1:
        queries_per_passage = 3
        logger.info(f"Automatically set `queries_per_passage` to {queries_per_passage}")

    #### Synthetic query generation ####
    #### This will be skipped if there is an existing `gen-queries.jsonl`file under `path_to_generated_data` ####

    if f"{qgen_prefix}-qrels" in os.listdir(
        path_to_generated_data
    ) and f"{qgen_prefix}-queries.jsonl" in os.listdir(path_to_generated_data):
        logger.info("Loading from existing generated data")
        corpus, gen_queries, _ = GenericDataLoader(
            path_to_generated_data, prefix=qgen_prefix
        ).load(split="train")
    else:
        logger.info("No generated queries found. Now generating it")
        assert "corpus.jsonl" in os.listdir(path_to_generated_data
        ), "At least corpus should exist!"
        qgen(
            data_path=path_to_generated_data,
            output_dir=path_to_generated_data,
            generator_name_or_path=generator,
            ques_per_passage=queries_per_passage,
            bsz=batch_size_generation,
            qgen_prefix=qgen_prefix,
        )
        corpus, gen_queries, _ = GenericDataLoader(
            path_to_generated_data, prefix=qgen_prefix
        ).load(split="train")

    #### Hard-negative mining ####
    #### This will be skipped if there is an existing `hard-negatives.jsonl` file under `path_to_generated_data` ####
    if "hard-negatives.jsonl" in os.listdir(path_to_generated_data):
        logger.info("Using exisiting hard-negative data")
    else:
        logger.info("No hard-negative data found. Now mining it")
        miner = NegativeMiner(
            path_to_generated_data,
            qgen_prefix,
            retrievers=retrievers,
            retriever_score_functions=retriever_score_functions,
            nneg=negatives_per_query,
        )
        miner.run()

    #### Pseudo labeling ####
    #### This will be skipped if there is an existing `gpl-training-data.tsv` file under `path_to_generated_data` ####
    gpl_training_data_fname = "gpl-training-data.tsv"
    if gpl_training_data_fname in os.listdir(path_to_generated_data):
        logger.info("Using existing GPL-training data")
    else:
        logger.info("No GPL-training data found. Now generating it via pseudo labeling")
        pseudo_labeler = PseudoLabeler(
            path_to_generated_data,
            gen_queries,
            corpus,
            gpl_steps,
            batch_size_gpl,
            cross_encoder,
            max_seq_length,
        )
        pseudo_labeler.run()



if __name__ == "__main__":
    data_dir = 'sample-data'
    querygen_gpl(
    path_to_generated_data=f'{data_dir}',
    batch_size_gpl=4,
    batch_size_generation=1,
    gpl_steps=1,
    queries_per_passage=3,
    # Number of Queries Per Passage (QPP) in the query generation step. When set to -1 (by default), 
    #the QPP will be chosen automatically: If QPP * |corpus| <= 250K, then QPP will be set to 250K / |corpus|; 
    #else QPP will be set 3 and |corpus| will be set to 250K / 3

    # QGen Models
    #generator="BeIR/query-gen-msmarco-t5-base-v1",
    generator="doc2query/msmarco-german-mt5-base-v1",
    #generator="svalabs/mt5-large-german-query-gen-v1",
    #generator="ml6team/mt5-small-german-query-generation",

    retrievers=["msmarco-distilbert-base-v3"], #, "msmarco-MiniLM-L-6-v3"],
    retriever_score_functions=["cos_sim", "cos_sim"],
    # Note that these two retriever model work with cosine-similarity
    cross_encoder="cross-encoder/ms-marco-MiniLM-L-6-v2",
    qgen_prefix="qgen",
    # This prefix will appear as part of the (fold
    # er/file) names for query-generation results: For example, we will have "qgen-qrels/" and "qgen-queries.jsonl" by default.
    )  

    #create training split for ML model from GPL data
    #format.create_train_test_eval_triples(data_dir)

