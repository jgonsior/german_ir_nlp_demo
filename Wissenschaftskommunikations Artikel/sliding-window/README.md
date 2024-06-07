# Generating sliding window PDF

This will create PDF documents containing every single word in a rectangular box. 

## Requirements

* Python >= 3.10
* pdflatex
* xelatex

## Install python packages

Package versions in `requirements.txt` have been well tested and you should use the versions specified.

```shell
pip install -r requirements.txt
```

## Why pdflatex / xelatex

Easy to use. Installs missing packages on the fly.

## How to install pdflatex / xelatex on windows?

1. Download and install MiKTeX from https://miktex.org/download
2. Locate `xelatex.exe` and `pdflatex.exe` in your installation folder. It should be located somewhere similar at `C:\Program\miktex\texmfs\install\miktex\bin\x64\xelatex.exe`
3. Copy `.env.EXAMPLE` to `.env`
4. Edit environment variable to path you found earlier. Example: `PATH_LATEX_COMPILER=C:\Program\miktex\texmfs\install\miktex\bin\x64\`. Or leave it empty to run `xelatex` and `pdflatex` command without a path if you specified it in your OS PATHS.
5. When running the code and you are asked to install missing packages for MiKTeX, accept the requests.

## Which files will be processed?

You need to specify the path of the file you want to process via `FILE_TO_PROCESS=` variable in `create_wordboxes.py`.

The file needs to be a JSON and must have the following format:

```json
[
  {
    "id": "DOC ID",
    "text": [
      "TEXT 1",
      "TEXT 2",
      "TEXT 3"
    ]
  },
  {
    "id": "DOC ID",
    "text": [
      "TEXT 1",
      "TEXT 2",
      "TEXT 3"
    ]
  },
  ...
]
```