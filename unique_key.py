import secrets
from django.db import IntegrityError

def gen_unique_key():
    try:
        unique_id = str(secrets.token_hex(8))
    except IntegrityError:
        self.gen_unique_key()
    return unique_id
