from flask import current_app

from flask_app import create_app
from flask_app.config import Developer, Production

app = create_app(config_class=Developer)

if __name__ == '__main__':
    app.run()#host='192.168.15.26')
