import os
import getpass
import base64
from hashlib import pbkdf2_hmac
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def kdf_pbkdf2_builtin(password, salt):
    dk = pbkdf2_hmac(
        hash_name="sha256",
        dklen=32,
        password=password.encode(encoding="utf-8"),
        salt=salt,
        iterations=500_000,
    )
    return dk


def kdf_pbkdf2_cryptography(password, salt):
    dk = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=500_000,
    )
    key = dk.derive(password.encode(encoding="utf-8"))
    return key


if __name__ == "__main__":
    p = getpass.getpass("Password: ")
    salt = os.urandom(16)
    print("salt: ", salt.hex())
    key = kdf_pbkdf2_builtin(p, salt)
    print("derived key using python builtin: ", key.hex())
    key2 = kdf_pbkdf2_cryptography(p, salt)
    print("derived key using cryptography lib: ", key2.hex())
