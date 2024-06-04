### Deploy Backend Server

Install Conda Environment:  [Miniconda](https://docs.anaconda.com/free/miniconda/)

```
# setup env
conda env create -f RAG_env_conda.yml
conda activate RAG_env

# deploy
python run.py
```

Die Flask API ist nun unter `localhost:8080` erreichbar und erwartet eine GET-Anfrage an dem Endpunkt `/search`

**Beispiel**
```
http://localhost:8080/search?q=Wer hat Snape ermordet?
```



