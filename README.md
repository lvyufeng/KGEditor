# KGEditor
a simple knowledge graph edit system backend implemented by flask

### How to use
#### 1.Install databases
1. mysql
2. redis
3. ArangoDB
#### 2. Configuration
```bash
cd your_path_to_project
# rename config.example.py to config.py, and modify the configuration of your own dbs
mv config.example.py to config.py
# create log folder
mkdir logs
# use manage.py to run
python manage.py runserver
```
----
### DB migration instructions

```bash
# init db
python manage.py db init
# generate migration script from modification
python manage.py db migrate -m "your message"
# execute migration
python manage.py db upgrade
```

### Celery usage

```bash
# start all celery tasks
celery -A tasks.main worker -l info
```
