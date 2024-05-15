# Preprocessing Setup

## Installing dependencies

```bash
python -m venv venv
pip install -r requirements_preprocessing.txt
```

## Executing `download_wikis.py` (IMPORTANT: To use the `download_wikis.py` file, you must use Python 3.9.X)

1. Add the required URLs to the Fandom Wiki(s) in `WIKI_DUMPS_URLS` (see template)

2. (Optional:) Adjust the `preprocessing_path` Path
3. Execute `python downloads_wikis.py`

## Executing `preprocess_wikis.py`

1. Adjust `WIKI_PATHS` to point to the correct directory that contains the `dumps/` files from `downloads_wikis.py`
2. Execute `python preprocess_wikis.py`

## (Optional) Removing Unicode characters

1. Adjust the `file_path` to point to the preprocessed `.json` file.
2. Execute `python process_unicode_characters.py`
