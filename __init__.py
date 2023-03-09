from flask import Flask

app=Flask(__name__)

@app.route("/")
def index():
    return "Hola mundo Codigo Facilito"


def inicializar_app(config):
    app.config.from_object(config)
    return app