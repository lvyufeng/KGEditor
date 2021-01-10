from kgeditor import create_app
from flask_script import Manager

app = create_app('develop')
manager = Manager(app)

if __name__ == '__main__':
    app.run()