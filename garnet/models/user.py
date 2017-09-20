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

    claims = ListField(StringField(max_length=120))

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
    # METHOD UPDATE PASSWORD
    # --------------------------------------------------------------------------
    def update_password(self, password):
        self.password = compute_hash(password, self.salt)
        return True

    # --------------------------------------------------------------------------
    # METHOD UPDATE EMAIL
    # --------------------------------------------------------------------------
    def update_email(self, email):
        """
            Updates the user's email with a new email.
            :param email: The new email address that is going to be assigned to the
                          user.
            :return: True if the email was updated successfully
        """
        self.email = email
        return True

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

    # --------------------------------------------------------------------------
    # METHOD ADD CLAIM
    # --------------------------------------------------------------------------
    def add_claim(self, claim):
        """
            Add a new claim to a given user and saves the new claim in the Database
            :param claim: The new claim to be added
            :return: True if claim was added, False if claim was no added to the
                     user.
        """
        if claim not in self.claims:
            self.claims.append(claim)
            return True
        else:
            return False


# ------------------------------------------------------------------------------
# GET USER BY ID
# ------------------------------------------------------------------------------
def get_user_by_id(user_id):
    """
        Tries to find a given instance of user by using its username. If the user
        exists and was found, an instance of user is returned, else, None is
        returned meaning that the system was unable to find a user with the given
        username.
    """
    try:
        user = User.objects.get(user_id=user_id)
        return user
    except DoesNotExist:
        app.logger.warning('A retrieval attempt of non-existing user occurred: ' + user_id)
    except MultipleObjectsReturned:
        app.logger.error('The username has more than 1 match in database. Urgent revision required. ' + user_id)
    return None


# ------------------------------------------------------------------------------
# GET USER BY USERNAME
# ------------------------------------------------------------------------------
def get_user_by_username(usrname):
    """
        Tries to find a given instance of user by using its username. If the user
        exists and was found, an instance of user is returned, else, None is
        returned meaning that the system was unable to find a user with the given
        username.
    """
    try:
        user = User.objects.get(username=usrname)
        return user
    except DoesNotExist:
        app.logger.warning('A retrieval attempt of non-existing user occurred: ' + usrname)
    except MultipleObjectsReturned:
        app.logger.error('The username has more than 1 match in database. Urgent revision required. ' + usrname)
    return None


# ------------------------------------------------------------------------------
# GET USER BY USERNAME
# ------------------------------------------------------------------------------
def get_user_by_email(email):
    """
        Tries to find a given instance of user by using its username. If the user
        exists and was found, an instance of user is returned, else, None is
        returned meaning that the system was unable to find a user with the given
        username.
    """
    try:
        user = User.objects.get(email=email)
        return user
    except DoesNotExist:
        app.logger.warning('A retrieval attempt of non-existing user occurred: ' + email)
    except MultipleObjectsReturned:
        app.logger.error('The username has more than 1 match in database. Urgent revision required. ' + email)
    return None