from garnet import app
from flask import jsonify, request
from garnet.models.user import build_account, get_user_by_username
from mongoengine import ValidationError, NotUniqueError
import sys


# --------------------------------------------------------------------------
# POST: /ACCOUNT
# --------------------------------------------------------------------------
@app.route('/account', methods=['POST'])
def post_account():

    # First we verify the request is an actual json request. If not, then we
    # responded with a HTTP 400 Bad Request result code.
    if not request.is_json:
        app.logger.warning('Request without JSON payload received on token endpoint')
        return jsonify({"msg": "Only JSON request is supported"}), 400

    # If we get here, is because the request contains valid json so we can
    # parse the parameters
    account_data = request.get_json()

    if 'username' in account_data and get_user_by_username(usrname=account_data['username']) is not None:
        return jsonify({
            "msg": "The provided username is not valid"
        }), 400

    user = build_account(account_data=account_data)

    # Now we verify that all required values are present and build a new instance
    # of user. If the instance is None, then one of the validations failed so
    # an HTTP BAD REQUEST status code should be returned
    if user is not None:
        # We try to create an instance
        try:
            # We try to persist the user account in Mongo Database

            print(user.to_dict())
            user.save()

            return jsonify({
                'user_id': user.user_id,
                'username': user.username
            }), 201
        except NotUniqueError as nue:
            app.logger.error(
                "A request tried to use an already existing username.")
            return jsonify({
                "msg": "Username or email are not available"
            }), 400
        except ValidationError as ve:
            app.logger.error(
                "An error occurred while trying to create a user account. Error: " + ve.message)
            return jsonify({
                "msg": "The request failed to validate"
            }), 400
        except:
            app.logger.error("An error occurred while trying to create a user account. Error: " + str(sys.exc_info()[0]))
            return jsonify({
                 "msg": "The server cannot complete the account creation process"
            }), 500
    else:
        return jsonify({
            "msg": "One or more of the required values is not present in the request"
        }), 400
