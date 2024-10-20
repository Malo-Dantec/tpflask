https://github.com/Malo-Dantec/tpflask.git

```
virtualenv -p python3 venv
source venv/bin/activate
```
```
pip install -r requirements.txt
```
```
flask loaddb tuto/data.yml
```
```
flask newuser identifiant mdp
```
```
Si vous voulez changer votre mot de passe : flask passwd identifiant nouveau_mdp
```
```
flask syncdb
```