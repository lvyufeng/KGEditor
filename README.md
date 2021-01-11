# KGEditer
a simple knowledge graph edit system implemented by flask

### how to use

```bash
# rename config.example.py to config.py, and modify the configuration of your own dbs
mv config.example.py to config.py
# use manage.py to run
python manage.py runserver
```
### db design

1. User
2. Domain
3. Project
4. Graph
5. Partner_Project

### db migration instructions

```bash
# init db
python manage.py db init
# generate migration script from modification
python manage.py db migrate -m "your message"
# execute migration
python manage.py db upgrade
```