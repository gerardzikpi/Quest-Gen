import sys
import os
from waitress import serve
from QuestGen import QuestGen

application =QuestGen.wsgi.application

def server():
    sys.path.append(os.path.abspath())
    if __name__ == '__main__':
        serve(application, host='[0.0.0.0]', port=8000)

server()