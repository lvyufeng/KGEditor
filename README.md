# KGEditer
a simple knowledge graph edit system implemented by flask

### how to use

```bash
# use manage.py to run
python manage.py runserver
```
### db design


### db migration instructions

```bash
# init db
python manage.py db init
# generate migration script from modification
python manage.py db migrate -m "your message"
# execute migration
python manage.py db upgrade
```