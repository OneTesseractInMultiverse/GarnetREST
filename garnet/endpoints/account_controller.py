from garnet import app
from flask import jsonify, request


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