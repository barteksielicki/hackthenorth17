import os

from .app import init_app

app = init_app(os.environ.get('APP_CONFIG'))
