"""Password hash wrapper"""

import bcrypt


class PasswordHash(object):
    """Wrap class for hash password comparsion

    Args:
        object (_type_): _description_
    """

    def __init__(self, hash_):
        # assert len(hash_) == 60, "bcrypt hash should be 60 chars."
        # assert hash_.count("$"), 'bcrypt hash should have 3x "$".'
        self.hash = str(hash_)
        self.rounds = int(self.hash.split("$")[2])

    def __eq__(self, candidate):
        """Hashes the candidate string and compares it to the stored hash."""
        if isinstance(candidate, str):
            print(candidate.encode("utf-8"))
            return bcrypt.checkpw(candidate.encode("utf-8"), self.hash)
            # return bcrypt.hashpw(candidate.encode("utf-8"), self.hash) == self.hash
        return False

    def __repr__(self):
        """Simple object representation."""
        return "<{}>".format(type(self).__name__)

    @classmethod
    def new(cls, password, rounds):
        """Creates a PasswordHash from the given password."""
        if isinstance(password, str):
            password = password.encode("utf-8")
        return cls(bcrypt.hashpw(password, bcrypt.gensalt(rounds)))
