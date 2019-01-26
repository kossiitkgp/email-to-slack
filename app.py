# -*- coding: utf-8 -*-
import os
import json
import requests

from flask import Flask, render_template, redirect, request, Response

app = Flask(__name__)


def validate(params):
    if params["event"]["type"] != "message":
        print("Event type is ", params["event"]["type"], "but not `message`")

    app_id = params["api_app_id"] == os.environ["APP_ID"]
    token = params["token"] == os.environ["VERIFICATION_TOKEN"]
    team = params["team_id"] == os.environ["TEAM_ID"]
    channel = params["event"]["channel"] == os.environ["USLACKBOT_CHANNEL"]
    user = params["event"].get("user", "") == "USLACKBOT"
    subtype = params["event"]["subtype"] = "file_share"

    if app_id and token and team and channel and user and subtype:
        return True
    else:
        return False


@app.route("/", methods=['GET', 'POST'])
def main():
    params = request.get_json(force=True)
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
    if request.method == "GET":
        return redirect("https://github.com/kossiitkgp/email-to-slack")
    elif request.method == "POST":

        print("parameters")
        print(json.dumps(request.get_json(force=True)))
        print("\n\n\n\nheaders\n\n\n\n")
        print(request.headers)
        params = request.get_json(force=True)

        if validate(params):
            email = params["event"]["files"][0]

            if f"CHECKED_{email['id']}" in os.environ or "X-Slack-Retry-Num" in request.headers:
                # This email has already been processed
                return Response(response="Duplicate", status=409)

            email_provider = "https://www.fastmail.com"

            sender_email = email["from"][0]["original"]
            email_subject = email["title"]
            email_content = "```" + email["plain_text"] + "```"
            timestamp = email["timestamp"]
            koss_logo_small = "https://raw.githubusercontent.com/kossiitkgp/design/master/logo/exported/koss-filled-small.png"

            data = {
                "text": "",
                "attachments": [
                    {
                        "fallback": "Something went wrong while displaying.",
                        "color": "#36a64f",
                        "pretext": "",
                        "author_name": sender_email,
                        "author_link": email_provider,
                        "author_icon": koss_logo_small,
                        "title": email_subject,
                        "title_link": email_provider,
                        "text": email_content,
                        "fields": [],
                        "footer": "email-to-slack",
                        "footer_icon": koss_logo_small,
                        "ts": timestamp
                    }
                ]
            }

            all_to = ', '.join([i["original"] for i in email["to"]])
            all_cc = ', '.join([i["original"] for i in email["cc"]])

            data["attachments"][0]["fields"].append({
                "title": "Sent To",
                "value": all_to
            })

            if all_cc:
                data["attachments"][0]["fields"].append({
                    "title": "cc",
                    "value": all_cc
                })

            if email["attachments"]:
                data["attachments"][0]["fields"].append({
                    "title": "",
                    "value": "This email also has attachments",
                    "short": False
                })

            INCOMING_WEBHOOK_URL = os.environ["INCOMING_WEBHOOK_URL"]

            headers = {
                "Content-type": "application/json"
            }

            r = requests.post(INCOMING_WEBHOOK_URL, headers=headers, json=data)

            # Slack API sends two payloads for single event. This is a bug
            # involving Heroku and Slack API.
            os.environ[f"CHECKED_{email['id']}"] = ''

            return Response(
                response="ok",
                status=200
            )
        else:
            return Response(
                response="Bad request",
                status=401
            )

        """
        Enable this to verify the URL while installing the app
        """

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

if __name__ == '__main__':
    app.run(debug=True)
