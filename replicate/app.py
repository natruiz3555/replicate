import os
from flask import Flask, request, redirect, render_template
from furl import furl
import awsgi
import requests

app = Flask(__name__)

CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]
CLIENT_SECRET = os.environ["GITHUB_CLIENT_SECRET"]
REPO = os.environ["GITHUB_REPO"]


@app.route("/", methods=["GET"])
def index():
    """Redirect to request for authorization"""
    authorize_url = furl("https://github.com/login/oauth/authorize").add({
        "client_id": CLIENT_ID,
        "scope": "public_repo"
    })
    return render_template("index.html", authorize_url=authorize_url)


@app.route("/callback", methods=["GET"])
def callback():
    """
    Handle the callback request from the user, and fork the repository. This
    expects the 'code' query parameter as the GitHub OAuth temporary code,
    and will redirect to the 'done' page if successful.
    """
    code = request.args["code"]
    access_token = authorize(code)
    fork_url = fork_repo(access_token)
    done_url = furl("done").add({"fork_url": fork_url})
    return redirect(done_url)


@app.route("/done", methods=["GET"])
def done():
    """Display the done page, with a link to the created repository."""
    return render_template("done.html", fork_url=request.args["fork_url"])


def fork_repo(access_token):
    """
    Create a fork the configured repository.

    :param access_token: The access token used to authorize this request.
    :type access_token: str
    :returns: The URL to the newly create repository.
    """
    headers = {
        "Authorization": "token {}".format(access_token)
    }

    response = requests.post(
        "https://api.github.com/repos/{}/forks".format(REPO),
        headers = headers
    )

    return response.json()["html_url"]


def authorize(callback_code):
    """
    Attempt to get an access key from the authorization code passed to the
    callback method.

    :param callback_code: The temporary code send by the client's browser that
                          we will use to get our access token.
    :type callback_code: str
    :returns: The access token from GitHub.
    """
    headers = {
        "Accept": "application/json"
    }
    authorization_data = {
        "code": callback_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post("https://github.com/login/oauth/access_token",
                             headers=headers,
                             data=authorization_data)
    response_json = response.json()
    return response_json["access_token"]


def lambda_handler(event, context):
    """This links lambda execution up to our WSGI app."""
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    app.run()
