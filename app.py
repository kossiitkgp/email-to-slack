# -*- coding: utf-8 -*-
import os
import json

from flask import Flask, render_template, redirect, request, Response


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def main():
        if request.method == "GET":
            return redirect("https://github.com/kossiitkgp/email-to-slack")
        elif request.method == "POST":
            # print("parameters")
            # print(json.dumps(request.get_json(force=True)))
            # print("headers")
            # print(request.headers)
            params = json.dumps(request.get_json(force=True))
            email = params["event"]["files"][0]

            INCOMING_WEBHOOK_URL = os.environ["INCOMING_WEBHOOK_URL"]

            headers = {
                "Content-type": "application/json"
            }


            sender_email = email["from"][0]["original"]
            email_file_link = email["url_private"]
            email_subject = email["title"]
            email_content = "```" + email["plain_text"] + "```"
            timestamp = email["timestamp"]
            koss_logo = "https://raw.githubusercontent.com/kossiitkgp/design/master/logo/exported/koss-logo.png"
            koss_logo_small = "https://raw.githubusercontent.com/kossiitkgp/design/master/logo/exported/koss-filled-small.png"

            data = {
                "text": f"\n*New mail in the inbox*! Click here : \n<{email_file_link}|Email>\n",
                "attachments": [
                    {
                        "fallback": email_file_link,
                        "color": "#36a64f",
                        "pretext": "Click on the file for better view. Although here are some details.",
                        "author_name": sender_email,
                        "author_link": email_file_link,
                        "author_icon": koss_logo_small,
                        "title": email_subject,
                        "title_link": email_file_link,
                        "text": email_content,
                        "fields": [
                            {
                                "title": "This message also has attachements",
                                "value": f"<{email_file_link}|View complete email>",
                                "short": True
                            }
                        ],
                        "footer": "email-to-slack",
                        "footer_icon": koss_logo_small,
                        "ts": timestamp
                    }
                ]
            }
            r = requests.post(INCOMING_WEBHOOK_URL, json=data)

            """
            Enable this to verify the URL while installing the app
            """

            # data = {
            #     'challenge': params.get('challenge'),
            # }
            # resp = Response(
            #     response=json.dumps(data),
            #     status=200,
            #     mimetype='application/json'
            # )
            # resp.headers['Content-type'] = 'application/json'

            # return resp

    app.secret_key = os.environ.setdefault("APP_SECRET_KEY", "notsosecret")
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = False
    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
