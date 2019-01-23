# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template, redirect, request

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def main():
        if request.method == "GET":
            return "Hello World"
        elif request.method == "POST":
            return "Hello World"

    app.secret_key = os.environ.setdefault("APP_SECRET_KEY", "notsosecret")
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = False
    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
