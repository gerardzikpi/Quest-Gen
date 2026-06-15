import os
import sys
from waitress import serve

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from QuestGen.wsgi import application


def server():
    serve(application, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    server()