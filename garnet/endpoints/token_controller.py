from garnet import app, jwt
from flask import jsonify, request
from garnet.models.user import get_user_by_username, get_user_by_id, User
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, \
    jwt_refresh_token_required, get_jwt_identity
import datetime


# --------------------------------------------------------------------------
# FUNCTION LOAD_CLAIMS
# --------------------------------------------------------------------------
@jwt.user_claims_loader
def load_claims(identity):
    """
        Given an identity, loads all the claims associated to that identity
        :param identity: The id of the user who's claims are going to be loaded.
               this functions assumes that the existence of the user in the user
               database has already being verified
        :return: A json serializable dictionary with the claims associated to the
                 given identity
    """
    user = get_user_by_id(identity)
    return {
        "is_application_user": True,
        "claims": user.claims
    }


# --------------------------------------------------------------------------
# REFRESH TOKEN ENDPOINT
# --------------------------------------------------------------------------
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_access_token():
    """
        If a valid refresh token is provided, then this endpoint creates a
        refreshed access token. Using refresh tokens can help preventing
        damage done when an access token is stolen. It is also important to
        consider the fact that if a refresh token is stolen, then he or her
        can continue requesting new access tokens for a given identity.

        :return: The new access token
    """
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


# --------------------------------------------------------------------------
# TOKEN ENDPOINT
# --------------------------------------------------------------------------
@app.route('/token', methods=['POST'])
def post_token():

    """
        Receives authentication credentials in order to generate an access
        token to be used to access protected models. Tokens generated
        by this endpoint are JWT Tokens.
    """

    # First we verify the request is an actual json request. If not, then we
    # responded with a HTTP 400 Bad Request result code.
    if not request.is_json:
        app.logger.warning('Request without JSON payload received on token endpoint')
        return jsonify({"msg": "Only JSON request is supported"}), 400

    # Read credentials from json request
    params = request.get_json()

    # Try to ready username and password properties. If one of them is not found,
    # then we generate an error and stop execution.

    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        app.logger.warning('Request without username parameter received on token endpoint')
        return jsonify({"msg": "A username parameter must be provided"}), 400
    if not password:
        app.logger.warning('Request without password parameter received on token endpoint')
        return jsonify({"msg": "A password parameter must be provided"}), 400

    # If we get here, is because a username and password credentials were
    # provided, so now we must verify them.

    user = get_user_by_username(username)

    if user is not None:
        if user.authenticate(password):

            # ACCESS TOKEN
            access_token_expires = datetime.timedelta(hours=2)
            access_token = create_access_token(identity=user.user_id, expires_delta=access_token_expires)

            # REFRESH TOKEN
            refresh_token_expires = datetime.timedelta(days=90)
            refresh_token = create_refresh_token(identity=user.user_id, expires_delta=refresh_token_expires)

            app.logger.info('A new token has been generated for user [' + user.user_id + "]")

            return jsonify({
                'access_token': access_token,
                'expiration': access_token_expires.total_seconds(),
                'refresh_token': refresh_token
            }), 200
    else:
        app.logger.warning('Request with invalid username was received')
        return jsonify({"msg": "Unable to find user with [" + username + "] username"}), 404
    

