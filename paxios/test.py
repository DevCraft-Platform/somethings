# ______   ___  __   __ _____  _____  _____   _               _ 
# | ___ \ / _ \ \ \ / /|_   _||  _  |/  ___| | |             | |
# | |_/ // /_\ \ \ V /   | |  | | | |\ `--.  | |_   ___  ___ | |_  ___
# |  __/ |  _  | /   \   | |  | | | | `--. \ | __| / _ \/ __|| __|/ __|
# | |    | | | |/ /^\ \ _| |_ \ \_/ //\__/ / | |_ |  __/\__ \| |_ \__ \
# \_|    \_| |_/\/   \/ \___/  \___/ \____/   \__| \___||___/ \__||___/
# =======================================================================
# Tests for the paxios package.

# _author_: INovomiast2 (Ivan Novomiast)
# _version_: 1.0.0
# _license_: MIT
# _github_: https://github.com/INovomiast2/paxios

# Importing the necessary modules
from paxios import fromFile, CreatePaxios, json
# Creating an instance of the CreatePaxios class

api = CreatePaxios(version=2, port=5500, debug=True, ssl=False, auth=False)

# This are some example routes.
@api.endpoint('/users', methods=['GET'])
def get_users():
	return api.json({'users': ['user1', 'user2', 'user3']})

# This is for testing taking the data from a file
@api.endpoint('/data', methods=['GET'])
def get_data():
    data = fromFile('test.json').read()
    return api.json(data)

# This is for testing POST requests
@api.endpoint('/postSomething', methods=['POST'])
def post_something():
    return api.json({'message': 'Data posted successfully!'})

@api.endpoint('/putSomething', methods=['PUT'])
def put_something():
    return api.json({'message': 'Data put successfully!'})

# Dynamic Routes are being under development
@api.endpoint('/dynamic/<name>', methods=['GET'])
def dynamic_route(name):
    return api.json({'name': name})

@api.endpoint('/dynamic/<name>/<age>', methods=['GET'])
def dynamic_route2(name, age):
    return api.json({'name': name, 'age': age})

# There are some routes that are pre-configured, like the oauth2 route
# This is for testing the pre-configured routes
@api.endpoint('/oauth2', methods=['GET'])
def oauth2():
    return api.json({'message': 'OAuth2 route'})

api.run()