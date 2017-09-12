from garnet import app
from flask import jsonify
    
# --------------------------------------------------------------------------
# ROOT RESOURCE OF THE API
# --------------------------------------------------------------------------
#
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "platform": "Garnet API 1.0",
        "version": "1.0",
        "message": "Garnet Satellite is now in Orbit!"
    })