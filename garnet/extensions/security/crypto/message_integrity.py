import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import AES


# --------------------------------------------------------------------------
# METHOD __COMPUTE_HASH
# --------------------------------------------------------------------------
# Computes the SHA256 hash of the given password and encodes the result into
# a hexadecimal string.
def compute_hash(password, salt):
    """
        Computes the SHA256 has value of a given password and encodes the
        using hex encoding to produce a readable string.

        :param password: The password to be hashed
        :param salt: A set of entropy data to prevent rainbow table and
                    dictionary attacks.
        :return: The resulting hash
    """
    return hashlib.sha256(password.encode('utf-8')+salt.encode('utf-8'))\
        .hexdigest()
