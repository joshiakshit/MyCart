import hashlib

import nacl.secret
import nacl.utils

from app.config import settings


def _derive_key(user_id: str | None = None) -> bytes:
    master = bytes.fromhex(settings.token_encryption_key)
    if user_id:
        return hashlib.blake2b(master, person=user_id.encode()[:16], digest_size=32).digest()
    return master[:32]


def encrypt_token(plaintext: str, user_id: str | None = None) -> bytes:
    key = _derive_key(user_id)
    box = nacl.secret.SecretBox(key)
    return box.encrypt(plaintext.encode("utf-8"))


def decrypt_token(ciphertext: bytes, user_id: str | None = None) -> str:
    key = _derive_key(user_id)
    box = nacl.secret.SecretBox(key)
    return box.decrypt(ciphertext).decode("utf-8")
