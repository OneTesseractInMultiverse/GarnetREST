import random
import string


# ------------------------------------------------------------------------------
# FUNCTION GEN_SALT
# ------------------------------------------------------------------------------
def gen_salt(length):
    """
        Generates a random set of data with a given length
        :param length:  The length og the random set
        :return: string randomly generated with a given length
    """
    return ''.join(random.SystemRandom()
                   .choice(string.ascii_uppercase + string.digits) for _ in range(length))


