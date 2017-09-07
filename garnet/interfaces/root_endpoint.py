from garnet import app
from flask import jsonify
    
# --------------------------------------------------------------------------
# ROOT RESOURCE OF THE API
# --------------------------------------------------------------------------
#
@app.route('/', methods=['GET'])
def get_root():
    return jsonify({
        "platform": "GarnetREST 1.0",
        "version": "1.0.0",
        "message": "Server is running!"
    })