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

if __name__ == "__main__":

    # https://<wiki-name>.fandom.com/wiki/Special:Statistics
    WIKI_DUMPS_URLS = {
        # films:
        "harry_potter": "https://s3.amazonaws.com/wikia_xml_dumps/d/de/deharrypotter_pages_current.xml",  # https://harrypotter.fandom.com/de/wiki/Spezial:Statistik
    }

    # create new directories for the data dumps in the data/ directory
    preprocessing_path = "backend/preprocessing/data"
    dump_path = os.path.join(preprocessing_path, "dumps")
    extraction_path = os.path.join(dump_path, "tmp")
    os.makedirs(extraction_path, exist_ok=True)

    for wiki_name, dump_url in WIKI_DUMPS_URLS.items():
        print("#" * 50)
        print(f"Starting to extract {wiki_name} wiki.")
        print("#" * 50, end="\n\n")
        # download the data dump into the data/fandoms/dumps directory
        dump_file_name = dump_url.split("/")[-1]
        path_to_dump_file = os.path.join(dump_path, dump_file_name)

        # this created many json like files in the extraction_path/AA directory
        print(f"Beginning to clean the {wiki_name} wiki.")
        cmd_str = f"python3 backend/preprocessing/wikiextractor/WikiExtractor.py --json -o {extraction_path} {path_to_dump_file}"
        subprocess.run(cmd_str, shell=True, check=True)

        # create dataframe and add the content of all data files to it
        df = pd.DataFrame()
        for root, dirs, files in os.walk(extraction_path):
            for f in files:
                path_f = os.path.join(root, f)
                df = pd.concat([df, pd.read_json(path_f, lines=True)], ignore_index=True, sort=False)
        print(f"{df.shape[0]} pages found!")

        # drop wiki pages which are to short
        # df = df[df.text.map(len) >= 50]
        # print(df.text.map(len).describe())
        # print(f"{df.shape[0]} pages remain after cleaning!")

        # save the dataframe to a json file
        wiki_json_file = os.path.join(dump_path, wiki_name) + "_raw.json"
        print(f"Saving {wiki_name} wiki to {wiki_json_file}.", end="\n\n\n")
        df.to_json(path_or_buf=wiki_json_file, orient="records", indent=1)

        # delete the tmp folder filled by temporary files from the wikiextractor
        shutil.rmtree(extraction_path)
        os.makedirs(extraction_path, exist_ok=True)

        # removes the unpacked data dump file to save disk space

    # finally remove the tmp folder
    shutil.rmtree(extraction_path)
