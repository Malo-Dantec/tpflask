https://github.com/Malo-Dantec/tpflask.git

```
virtualenv -p python3 venv
source venv/bin/activate
```
```
pip install flask
pip install python-dotenv
pip install bootstrap-flask
pip install flask-sqlalchemy
pip install flask-wtf
pip install flask-login
```




```
flask loaddb myapp/data.yml
```
```
flask syncdb
```