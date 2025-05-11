from src import create_app,db
from waitress import serve

app = create_app()

if __name__ == '__main__':
    print("Servidor iniciado en http://127.0.0.1:5000")
    serve(app, host='127.0.0.1', port=5000)
