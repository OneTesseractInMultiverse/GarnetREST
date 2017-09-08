from garnet import app, db
from flask import jsonify, request
from garnet.resources.token_resource import AccessToken

# --------------------------------------------------------------------------
# TOKEN ENDPOINT
# --------------------------------------------------------------------------
#
@app.route('/token', methods=['POST'])
def post_token():

    """
        Receives authentication credentials in order to generate an access
        token to be used to access protected resources. Tokens generated
        by this endpoint are JWT Tokens.
    """

    # First we verify the request is an actual json request. If not, then we
    # responded with a HTTP 400 Bad Request result code.
    if not request.is_json:
        return jsonify({"msg": "Only JSON request is supported"}), 400

    # Read credentials from json request
    params = request.get_json()

    # Try to ready username and password properties. If one of them is not found,
    # then we generate an error and stop execution.

    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "A username parameter must be provided"}), 400
    if not password
        return jsonify({"msg": "A password parameter must be provided"}), 400

    # If we get here, is because a username and password credentials were
    # provided, so now we must verify them.

    

