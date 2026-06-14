from waitress import serve
from QuestGen.wsgi import application

def server():
    if __name__ == '__main__':
        serve(application, host='[0.0.0.0]', port=8000)

server()