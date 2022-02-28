from nacl.utils import random as NCRandom
from nacl.secret import SecretBox as NCSecretBox
import binascii

def generate_nonce():
    nonce = NCRandom(NCSecretBox.NONCE_SIZE)
    return binascii.hexlify(nonce).decode()

def _sign_with_private_key(data):
    pass

def _sign_with_public_key(pub_key, data):
    pass

def _auth_verify():
    pass


def verify_key_validity(pub_key, message):
    pass
    

def verify_full_chain(pub_key, message):
    pass


def prepare_payload(message):
    pass
