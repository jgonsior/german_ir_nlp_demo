#!/usr/bin/env python3
import os
import shutil
import subprocess
import time
import urllib.request

import pandas as pd
from py7zr import unpack_7zarchive

# enables shutil to unpack 7zip files
shutil.register_unpack_format("7zip", [".7z"], unpack_7zarchive)

def extract_wiki_data(dump_file_path, extraction_path):
    """Extract wiki data from the dump file using WikiExtractor.

    Args:
        dump_file_path (str): The path to the dump file.
        extraction_path (str): The directory to save the extracted data.
    """
    cmd_str = f"python3 backend/preprocessing/wikiextractor/WikiExtractor.py --json -o {extraction_path} {dump_file_path}"
    subprocess.run(cmd_str, shell=True, check=True)

def load_extracted_data_to_df(extraction_path):
    """Load extracted data into a DataFrame.

    Args:
        extraction_path (str): The directory containing the extracted data files.

    Returns:
        pd.DataFrame: A DataFrame containing the combined data from all extracted files.
    """
    df = pd.DataFrame()
    for root, _, files in os.walk(extraction_path):
        for f in files:
            path_f = os.path.join(root, f)
            df = pd.concat([df, pd.read_json(path_f, lines=True)], ignore_index=True, sort=False)
    return df

def save_df_to_json(df, output_file):
    """Save the DataFrame to a JSON file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_file (str): The path to the output JSON file.
    """
    df.to_json(path_or_buf=output_file, orient="records", indent=1)

if __name__ == "__main__":
    WIKI_DUMPS_URLS = {
        # https://harrypotter.fandom.com/de/wiki/Spezial:Statistik
        "harry_potter": "https://s3.amazonaws.com/wikia_xml_dumps/d/de/deharrypotter_pages_current.xml",
    }

    preprocessing_path = "backend/preprocessing/data"
    dump_path = os.path.join(preprocessing_path, "dumps")
    extraction_path = os.path.join(dump_path, "tmp")
    os.makedirs(extraction_path, exist_ok=True)

    for wiki_name, dump_url in WIKI_DUMPS_URLS.items():
        print("#" * 50)
        print(f"Starting to extract {wiki_name} wiki.")
        print("#" * 50, end="\n\n")

        dump_file_name = dump_url.split("/")[-1]
        path_to_dump_file = os.path.join(dump_path, dump_file_name)

        print(f"Beginning to clean the {wiki_name} wiki.")
        extract_wiki_data(path_to_dump_file, extraction_path)

        df = load_extracted_data_to_df(extraction_path)
        print(f"{df.shape[0]} pages found!")

        wiki_json_file = os.path.join(dump_path, wiki_name) + "_raw.json"
        print(f"Saving {wiki_name} wiki to {wiki_json_file}.", end="\n\n\n")
        save_df_to_json(df, wiki_json_file)

        shutil.rmtree(extraction_path)
        os.makedirs(extraction_path, exist_ok=True)

    shutil.rmtree(extraction_path)