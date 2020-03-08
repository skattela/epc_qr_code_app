import os

import connexion
from connexion.exceptions import OAuthProblem
from flask import send_file

import epc_qrcode
import jira
import slack_bot

TOKEN_DB = {
    os.getenv("webhook_api_token"): {
        'uid': 0
    }
}


def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem('Invalid token')

    return info


def webhook(jira_ticket):
    if os.getenv("jira_url") and os.getenv("jira_user") and os.getenv("jira_api_token"):
        content = jira.get_issue_from_jira(jira_ticket)
        content["additional_text"] = "JIRA Ticket: %s", jira_ticket
        image = epc_qrcode.generate_epc_qrcode_with_info(content)
        image.save("epc_qrcode.png")
        file = open("epc_qrcode.png", "rb")
        jira.attach_to_jira(jira_ticket, file)
        if os.getenv("slack_api_token"):
            slack_bot.send_file_to_slack("epc_qrcode.png", title=jira_ticket, slack_channel=os.getenv("slack_channel"))
            return content, 200
        else:
            print("Slack integration not properly setup")
            return "Slack integration not properly setup", 500
    else:
        print("Jira integration not properly setup")
        return "Jira integration not properly setup", 500


def post_epc_qrcode(body):
    image = epc_qrcode.generate_epc_qrcode_with_info(body)
    image.save("epc_qrcode.png")
    file = open("epc_qrcode.png", "rb")
    return send_file("epc_qrcode.png", mimetype='image/png')


if __name__ == '__main__':
    if not os.getenv("webhook_api_token"):
        os.environ["webhook_api_token"] = "default"
        print("webhook_api_token was not set. setting it to 'default'")
    if os.getenv("jira_url") and os.getenv("jira_user") and os.getenv("jira_api_token"):
        print("jira integration active")
        if os.getenv("slack_api_token"):
            print("slack integration inactive")
        else:
            print("slack integration active")
    else:
        print("jira integration inactive")

    options = {'swagger_url': ''}
    app = connexion.App(__name__, options=options)
    app.add_api('openapi.yaml', arguments={'api_url': 'http://0.0.0.0:80'})
    app.run(port=80, server="tornado")
