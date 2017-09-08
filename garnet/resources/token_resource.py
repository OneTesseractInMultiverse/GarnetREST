from garnet import app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


# ------------------------------------------------------------------------------
# CLASS ACCESS TOKEN
# ------------------------------------------------------------------------------
class AccessToken:
    
    """
     ---------------------------------------------------------------------------
        Represents an AccessToken that can be generated, refreshed, has a linked
        identity and an expiration time. 
     ---------------------------------------------------------------------------
    """
    
    __identity = None
    __access_token = None
    __refresh_token = None