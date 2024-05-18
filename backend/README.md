### Deploy Backend Server

```
python -m venv venv
pip install -r requirements.txt

python run.py
```

Die Flask API ist nun unter `localhost:8080` erreichbar und erwartet eine GET-Anfrage an dem Endpunkt `/search`

**Beispiel**
```
http://localhost:8080/search?q=Suchbegriff
```



