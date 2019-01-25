# -*- coding: utf-8 -*-
import os
import json

from flask import Flask, render_template, redirect, request, Response

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def main():
        if request.method == "GET":
            return "Hello World"
        elif request.method == "POST":
            print("parameters")
            print(json.dumps(request.get_json(force=True)))

            print("headers")
            print(request.headers)

            params = request.get_json(force=True)
            print(params)
            data = {
                'challenge': params.get('challenge'),
            }
            resp = Response(
                response=json.dumps(data),
                status=200,
                mimetype='application/json'
            )
            resp.headers['Content-type'] = 'application/json'

            return resp

    app.secret_key = os.environ.setdefault("APP_SECRET_KEY", "notsosecret")
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = False
    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
