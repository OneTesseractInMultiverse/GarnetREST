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


# --------------------------------------------------------------------------
# AES CIPHER
# --------------------------------------------------------------------------
class AESCipher(object):

    """
        This class provides AES Encryption and Decryption
    """

    # ----------------------------------------------------------------------
    # CONSTRUCTOR METHOD
    # ----------------------------------------------------------------------
    def __init__(self, key):
        """
            Creates an instance of AESCipher class
            :param key: The encryption/decryption key
        """
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    # ----------------------------------------------------------------------
    # METHOD ENCRYPT
    # ----------------------------------------------------------------------
    def encrypt(self, raw):
        """

        :param raw:
        :return:
        """
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    # ----------------------------------------------------------------------
    # METHOD DECRYPT
    # ----------------------------------------------------------------------
    def decrypt(self, cipher_text):
        """
            Runs the decryption function over a given cipher-text
            :param cipher_text: The encrypted message
            :return: If the decryption key is correct, the decrypted data
        """
        cipher_text = base64.b64decode(cipher_text)
        iv = cipher_text[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(cipher_text[AES.block_size:])).decode('utf-8')

    # ----------------------------------------------------------------------
    # METHOD PAD
    # ----------------------------------------------------------------------
    def _pad(self, s):
        """
            Appends some data at the end of a
            :param s: The size of the pad
            :return: A message with additional padding added at the end
        """
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    # ----------------------------------------------------------------------
    # METHOD UNPAD
    # ----------------------------------------------------------------------
    @staticmethod
    def _unpad(s):
        """
            Removes the padding at the end of a message
            :param s: The size of the pad
            :return: The message without the padding at the end
        """
        return s[:-ord(s[len(s)-1:])]