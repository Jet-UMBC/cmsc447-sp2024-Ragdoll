import os

from flask import Flask
from scores.home import home
from scores.update import update
from scores.create import create

#Reset Database by running flask --app scores init-db. 
#THIS DELETES ALL DATA. BE CAREFUL

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'scores.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(home)
    app.register_blueprint(create)
    app.register_blueprint(update)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'    

    from . import database
    database.init_app(app)


    return app