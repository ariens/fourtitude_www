import bcrypt

inputMismatchError = TypeError("inputs must be both bytes")


def constant_time_compare(a, b):
    """
    Examines two bytes items and returns True if they are identical or false if not
    Performs a full comparison without returning early upon first identified inequality
    Adapted from http://throwingfire.com/storing-passwords-securely/
    :param a: the first bytes item
    :param b: the second bytes item
    :return: True or False
    :raise inputMismatchError:
    """
    if isinstance(a, bytes):
        if not isinstance(b, bytes):
            raise inputMismatchError
    else:
        raise inputMismatchError
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0


def get_digest(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_password(password, digest):
    challenge = bcrypt.hashpw(password, digest)
    return constant_time_compare(challenge.encode('utf-8'), digest.encode('utf-8'))