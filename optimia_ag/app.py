from flask import Flask
from controllers.record_controller import *

app = Flask(__name__)

app.register_blueprint(record_api)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)