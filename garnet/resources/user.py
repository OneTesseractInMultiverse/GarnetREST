from garnet import app
from garnet.extensions.security.entropy import gen_salt
from garnet.extensions.security.gcrypt import compute_hash
from werkzeug.security import safe_str_cmp
from mongoengine import *
import datetime


# ------------------------------------------------------------------------------
# CLASS USER
# ------------------------------------------------------------------------------
class User(Document):

    """
        Represents a User in the system. And a document type in MongoDb. All
        attributes that belong to a given user of the system go here.
    """

    # --------------------------------------------------------------------------
    # USER PROPERTIES
    # --------------------------------------------------------------------------

    user_id = StringField(max_length=40, required=True)

    name = StringField(max_length=120, required=True)

    last_name = StringField(max_length=120, required=True)

    email = StringField(max_length=120, required=True, unique=True)

    username = StringField(max_length=120, required=True, unique=True)

    password = StringField(max_length=256, required=True)

    salt = StringField(max_length=17, required=True, default=gen_salt(17))

    date_modified = DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': [
            'user_id',
            'username',
            'email'
        ]
    }

    # --------------------------------------------------------------------------
    # METHOD AUTHENTICATE
    # --------------------------------------------------------------------------
    def authenticate(self, password):
        """
            Compares the given password in a secure way with a value stored in
            database to determine if the password is correct or not.

            :param password: The password to be verified if it is the correct password
                   for the given user.
            :return: True if the authentication was successful and the password is
                     correct
        """
        challenge = compute_hash(password, self.salt)
        return safe_str_cmp(self.password.encode('utf-8'), challenge.encode('utf-8'))

    # --------------------------------------------------------------------------
    # METHOD DICT
    # --------------------------------------------------------------------------
    def to_dict(self):
        """
            Generates a dictionary representing the current state of the user
            entity.
            :return: A dictionary of the current state of te entity
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username,
            "date_modified": self.date_modified
        }

    # --------------------------------------------------------------------------
    # METHOD LOAD
    # --------------------------------------------------------------------------
    def load(self, state):
        """
            Loads a given state in a dictionary into the User entity
            :param state: A dictionary containing the state to be loaded
            :return: Nothing
        """
        self.date_modified = state["date_modified"]
        self.username = state["username"]
        self.email = state["email"]
        self.last_name = state["last_name"]
        self.name = state["name"]
        self.user_id = state["user_id"]
        return


# ------------------------------------------------------------------------------
# GET USER BY ID
# ------------------------------------------------------------------------------
def get_user_by_id(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        return user
    except DoesNotExist:
        app.logger.warning('A retrieval attempt of non-existing user occurred: ' + user_id)
    except MultipleObjectsReturned:
        app.logger.error('The username has more than 1 match in database. Urgent revision required. ' + user_id)
    return None