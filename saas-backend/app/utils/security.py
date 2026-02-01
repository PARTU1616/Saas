from werkzeug.security import generate_password_hash as _gen, check_password_hash as _check
from hashlib import sha256

def hash_token(token: str) -> str:
    return sha256(token.encode()).hexdigest()



def generate_password_hash(password: str) -> str:
	"""Return a salted hash for the given password.

	Uses Werkzeug's generate_password_hash with a reasonable default.
	"""
	return _gen(password)

def check_password_hash(stored_hash: str, password: str) -> bool:
	"""Return True if password matches stored_hash."""
	return _check(stored_hash, password)
