# -*- coding: utf-8 -*-

import os

from flask import Flask, jsonify

from helpers import get_temperature, send_temperature

application = Flask(__name__)


@application.route("/")
def hello():
    # This mocks MQTT integration
    send_temperature(get_temperature())

    return jsonify(
        {
            "object": f"{os.getenv('app_name')}",
            "temperature": f"{get_temperature()} Celsius"
        }
    )


if __name__ == "__main__":
    # Only for debugging while developing
    application.run(host='0.0.0.0', debug=False)
