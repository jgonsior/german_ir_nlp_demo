#!/usr/bin/env python3

import json
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, PreTrainedTokenizerFast, T5ForConditionalGeneration, LlamaForCausalLM, LlamaTokenizer, LlamaTokenizerFast, BitsAndBytesConfig, pipeline, set_seed
from peft import PeftModel
import torch
import math
from time import time_ns, sleep
import gc
from tqdm import tqdm

class TranslatorGer2En():
    def __init__(self, device="cuda"):
        self.tokenizer, self.model = load_llm("llama2-ger2en")
        self.device = device

    def translate(self, docs, batchsize=10):
        batches = batch(docs, batchsize)
        output = []
        for b in tqdm(batches):
            inputs = [doc + " ###>" for doc in b]
            t0 = time_ns()
            model_inputs = tokenize(inputs, self.tokenizer, device=self.device, padding=True, truncation=False)
            t1 = time_ns()
            outputs = self.model.generate(**model_inputs, max_new_tokens=500, pad_token_id=self.tokenizer.pad_token_id, num_beams=5)
            t2 = time_ns()
            outputs = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
            t3 = time_ns()
            tokenization_time = (t1-t0)*1e-6
            generation_time = (t2-t1)*1e-6
            decoding_time = (t3-t2)*1e-6
    #        print(f"Tokenization: {tokenization_time} ms\nGeneration: {generation_time} ms\nDecoding: {decoding_time} ms")
            outputs = [o.split("###>")[1].strip() for o in outputs]
            for o in outputs:
                output.append(o)
        return output

class QueryGenerator():
    def __init__(self, device="cuda"):
        self.tokenizer, self.model = load_llm("flan")
        self.device = device

    def qgen(self, docs, batchsize=10):
        prompt = "Let the following be a document, about which a query is to be formulated. Dereference any indirect mentions to make sure no additional context is required. Document: {}; Query: "
        docs = [prompt.format(d) for d in docs]
        batches = batch(docs, batchsize)
        output = []
        for b in tqdm(batches):
            model_inputs = tokenize(b, self.tokenizer, device=self.device, padding=True, truncation=False)
            outputs = self.model.generate(**model_inputs, max_new_tokens=200, do_sample=True)
            outputs = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
            for o in outputs:
                output.append(o)
        return output

class TranslatorEn2Ger():
    def __init__(self, device="cuda"):
        self.en2ger = pipeline('translation', model='Tanhim/translation-En2De', tokenizer='Tanhim/translation-En2De')

    def translate(self, docs):
        output = []
        for d in tqdm(docs):
            query_ger = self.en2ger(d)[0]["translation_text"]
            output.append(query_ger)
        return output

def main():
    tl = TranslatorGer2En()
    docs, ids, _ = load_docs("data/harrypotter/corpus.jsonl")

    t0 = time_ns()
    outputs = tl.translate(docs, batchsize=2)
    t1 = time_ns()
    print(f"Translating Ger2En took {(t1-t0)*1e-9} s")
#    print(outputs)
    del(tl)
    clean_gpu_memory()

    qg = QueryGenerator()
    t0 = time_ns()
    outputs = qg.qgen(outputs, batchsize=5)
    t1 = time_ns()
    print(f"Generating Queries took {(t1-t0)*1e-9} s")
#    print(outputs)
    del(qg)
    clean_gpu_memory()

    tl = TranslatorEn2Ger()
    t0 = time_ns()
    outputs = tl.translate(outputs)
    t1 = time_ns()
    print(f"Translating Queries took {(t1-t0)*1e-9} s")
#    print(outputs)

    write_queries(outputs, ids)

def batch(docs, bsz):
#    if bsz == 1:
#        return docs
#    else:
    return [docs[bsz * i : bsz * i + bsz] for i in range(len(docs) // bsz + math.ceil((len(docs) % bsz) / bsz))]

def clean_gpu_memory():
    torch.cuda.empty_cache()
    gc.collect()

def gen_queries_gpl(data_in=".", data_out=".", prefix="qgen", qpp=3, model="models/flan-ul2/"):
    import gpl
    # qgen(data path, output path, ...)
    gpl.toolkit.qgen(data_in, data_out, qgen_prefix=prefix, ques_per_passage=qpp, bsz=16, generator_name_or_path=model)

def write_queries(queries, orig_ids):
    with open("output/qgen-queries.jsonl", "w") as f:
        with open("output/qrels.tsv", "w") as g:
            g.write("query-id\tcorpus-id\tscore\n")
            for idx, q in enumerate(queries):
                qdict = {"_id": "genQ" + str(idx), "text": q}
                f.write(json.dumps(qdict, ensure_ascii=False) + "\n")
                g.write("genQ" + str(idx) + "\t" + orig_ids[idx] + "\t1\n")

def load_docs(data_in):
    # expect data_in to be a beir-compatible jsonl file, just like the corpus.jsonl (but a different name is ok)
    with open(data_in, "r") as f:
        docs = []
        ids = []
        titles = []
        for line in f.readlines():
            docs.append(json.loads(line)["text"])
            ids.append(json.loads(line)["_id"])
            titles.append(json.loads(line)["title"])

    return docs, ids, titles

def load_llm(modelname, device="cuda"):
    match modelname:
        case "flan":
            modelpath = "models/flan-ul2"
            tokenizer = AutoTokenizer.from_pretrained(modelpath, use_default_system_prompt=False)
            compute_dtype = getattr(torch, "float16")
            bnb_config = BitsAndBytesConfig(load_in_4bit=False, bnb_4bit_compute_dtype=compute_dtype)
            model = T5ForConditionalGeneration.from_pretrained(modelpath, torch_dtype=torch.float16, device_map=device, quantization_config=bnb_config)

        case "llama2":
            modelpath = "models/Llama-2-13B"
            tokenizer = LlamaTokenizerFast.from_pretrained(modelpath, use_default_system_prompt=False)
            model = LlamaForCausalLM.from_pretrained(modelpath, torch_dtype=torch.bfloat16, device_map=device, attn_implementation="flash_attention_2", load_in_4bit=False)

        case "llama2-ger2en":
            modelpath = "models/Llama-2-7B"
            compute_dtype = getattr(torch, "float16")
            bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=compute_dtype, bnb_4bit_use_double_quant=True)
            model = AutoModelForCausalLM.from_pretrained(modelpath, device_map=device, quantization_config=bnb_config)
            tokenizer = AutoTokenizer.from_pretrained(modelpath, use_fast=True, pad_token="</s>", padding_side="left", max_length=4096)
            model = PeftModel.from_pretrained(model, "kaitchup/Llama-2-7b-mt-German-to-English")

        case "llama3":
            modelpath = "models/Llama-3-8B"
            tokenizer = PreTrainedTokenizerFast.from_pretrained(modelpath, use_default_system_prompt=False)
            tokenizer.add_special_tokens({"pad_token":"<pad>"})
            terminators = [
                tokenizer.eos_token_id,
                tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]
            model = LlamaForCausalLM.from_pretrained(modelpath, torch_dtype=torch.bfloat16, device_map=device, attn_implementation="flash_attention_2", load_in_4bit=False)

    return tokenizer, model

def tokenize(input, tokenizer, device="cuda", padding=False, truncation=False):
    return tokenizer(input, padding=padding, truncation=truncation, return_tensors="pt").to(device)

def translate_ger2en(text, tokenizer, model):
    prompt = text + " ###>"
    model_input = tokenize(prompt, tokenizer)
    num_tokens = model_input["input_ids"].shape[-1]
    output = model.generate(**model_input, max_new_tokens=500, pad_token_id=tokenizer.eos_token_id, num_beams=10)
    output = tokenizer.decode(output[0][num_tokens:], skip_special_tokens=True)
    return output

def generate_query(text, tokenizer, model):
    model_input = tokenize(text, tokenizer)
    output = model.generate(**model_input, max_new_tokens=200, do_sample=True)
    output = tokenizer.decode(output[0], skip_special_tokens=True)
    return output

def main2():
### Load Corpus
    # docs = load_docs("data/witcher/corpus.jsonl")
    docs = load_docs("data/harrypotter/corpus.jsonl")
    corpus_lang = "ger"
    # print(docs[:10])

### Load Models
    flan_tokenizer, flan_model = load_llm("flan")
    if corpus_lang == "ger":
        llama_ger2en_tokenizer, llama_ger2en_model = load_llm("llama2-ger2en")
    en2ger = pipeline('translation', model='Tanhim/translation-En2De', tokenizer='Tanhim/translation-En2De')
    set_seed(42)

### Prompts
    # prompt = "Let the following be a document, about which a query is to be formulated. The query must not rely on further context or information. Document: {}; Query: "
    # prompt = "Translate the following document to German! Document: {}; Translation: "
    prompt = "Let the following be a document, about which a query is to be formulated. Dereference any indirect mentions to make sure no additional context is required. Document: {}; Query: "

### Main Loop
    for d in docs[:10]:
        if corpus_lang == "ger":
            d_ger = d
            d = translate_ger2en(d, llama_ger2en_tokenizer, llama_ger2en_model)
        elif corpus_lang == "en":
            d_ger = en2ger(d)[0]["translation_text"]

        query_en = generate_query(prompt.format(d), flan_tokenizer, flan_model)
        query_ger = en2ger(query_en)[0]["translation_text"]
        print("Dokument: " + d_ger + "\n" +
              "Document: " + d + "\n" +
              "Query:    " + query_en + "\n" +
              "Anfrage:  " + query_ger + "\n\n")

if __name__ == "__main__":
    main()
