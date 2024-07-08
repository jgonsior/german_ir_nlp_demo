#!/bin/bash

FOLDER_PATH=$1
OUTPUT_PATH=$2

if [ -z "$FOLDER_PATH" ]; then
  echo "No folder path provided."
  exit 1
fi

for file in "$FOLDER_PATH"/*.tex; do
  pdflatex -interaction=batchmode -output-directory="$OUTPUT_PATH" --shell-escape "$file"
done