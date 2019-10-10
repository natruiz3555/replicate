# Specification #

The 'replicate' application automatically forks a configured repository into the
account of an authorized GitHub user. When configured to fork it's own
repository it becomes a self-replicating GitHub repository.

This requires the use of OAuth to allow our application to access the GitHub API
on the user's behalf. This is the general data flow of the app:

![Data flow diagram](data_flow_diagram.svg)

## How it works ##
We are using the Python web framework, 'Flask', to handle the web requests
required in this program.

### End-points #
These are the end-points used:

#### `GET /` ####
This end-point returns a HTML page displaying a Welcome message, along with a
link to begin the authorization process. This is intended to be the starting
point for new users.

#### `GET /callback` ####
This end-point deals with confirming the application's authorization with
GitHub, and then forking the GitHub repository into the user's account.

This expects the `code` query parameter to be passed in, which should be filled
in by GitHub's redirect after the user authorizes the application.

If all operations succeed, then the user will be redirected to the `/done`
method, with the URL of the newly created GitHub repository passed in as a query
parameter.

#### `GET /done` ####
This end-point displays a success message to the user, as well as a link to
their new GitHub repository. In order to get the GitHub repository URL, we
expect the `fork_url` query parameter to be set to it's URL.

### Interaction with GitHub ###
There are three ways our application interacts with GitHub:

#### Authorization redirect ####
Our application redirects to GitHub to ask the user to give us authorization to
use specific functions on their API. The scope we use is `public_repo`, since it
allows access to create a fork, but not to access private repositories.

The request URL we direct the user to is:
`https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&scope=public_repo`,
where `{CLIENT_ID}` is the client ID of the GitHub OAuth application.

#### Request access token ####
Once we get our temporary user code, we need to convert it into an access token
that we can use to make requests to GitHub's API. For that, we make a request to
the following end-point:
```
POST https://github.com/login/oauth/access_token
```
with the extra header:
```
Accept: application/json
```
with the body data:
```
code={CODE}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}
```
where `{CLIENT_ID}` and `{CLIENT_SECRET}` are the client ID and the client
secret of the GitHub OAuth application respectively, and `{CODE}` is the
temporary user code.

The response for a successful request is a JSON object containing the key
`access_token`, which we can use to authorize future API requests.

#### Fork repository ####
When we get an access token, we can actually fork the repository by making a
request to the end-point:
```
POST https://api.github.com/repos/{owner}/{repo}/forks
```
with the extra header:
```
Authorization: token {access_token}
```
where `{owner}` and `{repo}` are the owner and repository that we want to fork
respectively.

In the response JSON object for this request, we can use the `html_url` to get
the newly created repository URL.