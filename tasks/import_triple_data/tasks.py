from tasks.main import celery_app as app

@app.task
def open_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        print(f.readline())
    f.close()

    return 1

# read data from csv or json file

# save them into arangodb


