from flask import Flask
from src.routes import index

app = Flask(__name__, static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def index_route():
    return index()


if __name__ == '__main__':
    """
    Запускает Flask-приложение. Создает директорию для статических файлов, если она не существует.
    """
    app.run(host='0.0.0.0', port=8000, debug=True)
