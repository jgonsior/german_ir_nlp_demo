import os
import csv
import json
import random
import inspect

def map_json(file_name: str, key: str, value: str):
    """
    mapping two values in json object

    Arguments:
        file_name -- path of json file
        key -- value which should be key
        value -- value attribute for the key

    Returns:
        map with mapping of two values as key-value pair
    """   
    with open(file_name, "r") as f:
        map = {}
        for obj in f:
            obj = json.loads(obj)
            key_obj = obj[key]
            value_obj = obj[value]
            map[key_obj] = value_obj
        return map



def format_to_data(dir: str):
    """
    Function for formatting the training data generated by GPL Toolkit into training data for ColBERT

    Returns:
        List of json objects with {"query": query, "pos": [pos_pas], "neg": [neg_pas]}
    """
    abs_path_caller = os.path.dirname(inspect.stack()[1][1])
    work_dir = f"{abs_path_caller}/{dir}"

    write_data = []
    with open(f"{work_dir}/hard-negatives.jsonl", 'r') as file:

        query_map = map_json(f"{work_dir}/qgen-queries.jsonl", "_id", "text")
        corpus_map = map_json(f"{work_dir}/corpus.jsonl", "_id", "text")

        for json_object in file:
            write_object = {}
            data = json.loads(json_object)

            qid = data["qid"]
            write_object["question"] = query_map[qid]
            
            pos_id = data["pos"][0]
            write_object["positive_contexts"] = [corpus_map[pos_id]]
            write_object["positive_context_ids"] = [pos_id]

            neg_ids = data["neg"]["msmarco-distilbert-base-v3"]
            neg_list = [corpus_map[id] for id in neg_ids]
                                      
            write_object["negative_contexts"] = neg_list
            write_object["negative_context_ids"] = neg_ids
            write_data.append(write_object)

    with open(f"{work_dir}/data.json", "w", encoding="utf-8") as file:
        json.dump(write_data, file, indent = 1, ensure_ascii=False)


def jsonl_to_json(file: str):
    """
    convert jsonl to json file, used for gpl jsonl generation
    """
    abs_path_caller = os.path.dirname(inspect.stack()[1][1])
    work_file = f"{abs_path_caller}/{file}"

    jsons=[]

    with open(work_file, "r") as f:
        for obj in f:
            jsons.append(json.loads(obj))

    file_name = file.strip(".jsonl")
    output_file = f"{abs_path_caller}/{file_name}.json"
    with open(output_file, "w", encoding = "utf-8") as output:
        json.dump(jsons, output, indent = 1, ensure_ascii = False)

def corpus_json_to_csv(dir: str):
    """
    write passages.csv from corpus.jsonl as input

    passages.csv: id, passage_text
    """
    abs_path_caller = os.path.dirname(inspect.stack()[1][1])
    work_dir = f"{abs_path_caller}/{dir}"

    with open(f"{work_dir}/corpus.jsonl", "r") as jsonl_file, open(f"{work_dir}/passages.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["id", "passage_text"])

        for obj in jsonl_file:
            data = json.loads(obj)
            del data["title"]
            writer.writerow(data.values())


def create_train_eval_test_triples(dir: str):
    """
    split data from 'format_to_data' function into train, test, and eval
    """
    abs_path_caller = os.path.dirname(inspect.stack()[1][1])
    work_dir = f"{abs_path_caller}/{dir}"

    with open(f"{work_dir}/data.json", "r") as file:
        data = json.load(file)
        
    random.shuffle(data)

    total_len = len(data)
    train_len = int(0.8 * total_len)
    eval_test_len = int(0.1 * total_len)

    train_data = data[:train_len]
    eval_data = data[train_len:(train_len + eval_test_len)]
    test_data = data[train_len + eval_test_len:]

    with open(f"{work_dir}/train_triples.jsonl", "w", encoding="utf-8") as file:
        for obj in train_data:
            json.dump(obj, file, ensure_ascii=False)
            file.write("\n")

    with open(f"{work_dir}/eval_triples.jsonl", "w", encoding="utf-8") as file:
        for obj in eval_data:
            json.dump(obj, file, ensure_ascii=False)
            file.write("\n")

    with open(f"{work_dir}/test_triples.jsonl", "w", encoding="utf-8") as file:  
        for obj in test_data:
            json.dump(obj, file, ensure_ascii=False)
            file.write("\n")
