import os
import subprocess

import connexion
from connexion.exceptions import OAuthProblem

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


def update():
    subprocess.call("deploy.sh")


if __name__ == '__main__':
    if not os.getenv("webhook_api_token"):
        os.environ["webhook_api_token"] = "default"
        print("webhook_api_token was not set. setting it to 'default'")

    options = {'swagger_url': ''}
    app = connexion.App(__name__, options=options)
    app.add_api('openapi.yaml', arguments={'api_url': 'http://0.0.0.0:88'})
    app.run(port=88, server="tornado")
