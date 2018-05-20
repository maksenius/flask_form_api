import os

from app import create_app
from config import CURRENT_CONFIG

app = create_app(CURRENT_CONFIG)

if __name__ == '__main__':
    app.run()
