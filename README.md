https://github.com/Malo-Dantec/tpflask.git

```
virtualenv -p python3 venv
source venv/bin/activate
```
```
pip install -r requirements.txt
```
```
flask loaddb myapp/data.yml
```
```
flask syncdb
```