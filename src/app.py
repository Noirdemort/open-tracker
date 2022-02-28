from flask import Flask, request, jsonify
import json
import logging
from controller import usr_api_blueprint

logging.basicConfig(filename='local.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 # restricts request size to 20 MB
app.register_blueprint(usr_api_blueprint, url_prefix="/api/v1")


@app.route("/<path:path>", methods=["OPTIONS"])
def handleOptions(path):
    return "", 204

@app.route("/")
def index():
    return jsonify({"message": "hello world"})
        
# TODO: Enable CORS if getting error
# @app.after_request
# def add_cors(response):
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = '*'
#     header['Access-Control-Allow-Headers'] = '*'
#     header['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, PUT'
#     return response

if __name__ == '__main__':
    app.run()
