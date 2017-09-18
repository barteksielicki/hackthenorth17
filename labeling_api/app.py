from flask import Flask

from .db import db
from .config import CONFIG_MAPPING
from .flask_restful_extensions import (
    Api,
    API_RESOURCES_REGISTER,
)
from .resources import *


def init_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAPPING.get(
        config_name,
        CONFIG_MAPPING.get('default'),
    ))
    api = Api(app, catch_all_404s=True)
    api.add_resources(API_RESOURCES_REGISTER)
    db.init_app(app)
    return app
