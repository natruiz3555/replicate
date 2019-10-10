# Self replicating GitHub repository #

This project forks an existing repository on behalf of a user authorized with
GitHub OAuth. It doesn't require access to a user's private repositories since
it only requests access to the `public_repo` scope.

To set this up on your own system, you'll need to create a new OAuth app on
GitHub, and use it's client_id and client_secret. Follow these instruction if
you need help:
https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/.

## Demo ##

Try it out here: https://replicate.jitb.tk/

## Running ##

You can run this one your local system by running the following. These
instructions were tested on Debian 9, with Python 3.5 installed:

```bash
git clone https://github.com/natruiz3555/replicate.git
cd replicate
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt

export GITHUB_CLIENT_ID=<your_github_client_id>
export GITHUB_CLIENT_SECRET=<your_github_client_id>
export GITHUB_REPO=natruiz3555/replicate # Or another repository of your choice.

python replicate/app.py
```

## Building package for AWS Lambda ##

Follow these steps to produce a AWS Lambda zip package:
```bash
git clone https://github.com/natruiz3555/replicate.git
cd replicate

# This gets around issues with pip --target on Debian based systems.
# See https://github.com/pypa/pip/issues/3826 for more info.
virtualenv -p python3 venv
. venv/bin/activate

# Build the lambda zip.
pip install --target package .
cp lambda_function.py package/
chmod -R 755 package/
cd package/
zip -r9 ../function.zip .
```