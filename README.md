# KGEditer
a simple knowledge graph edit system implemented by flask

### how to use

```bash
# use manage.py to run
python manage.py runserver
```
### db design

1. User
2. Domain
3. Project
4. Graph
<<<<<<< HEAD
5. Partner_Project
=======
>>>>>>> 43e362330d293e1be9927df0656450e865c532b2

### db migration instructions

```bash
# init db
python manage.py db init
# generate migration script from modification
python manage.py db migrate -m "your message"
# execute migration
python manage.py db upgrade
```