# pip install cryptography msgpack
import os, struct, msgpack
from typing import Dict, Any, Tuple
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidTag as CryptoInvalidTag

# ========= Exceptions =========
class EncryptionError(Exception): pass
class DecryptionError(Exception): pass
class HeaderError(DecryptionError): pass
class UnsupportedVersion(DecryptionError): pass
class UnknownProfile(DecryptionError): pass
class IntegrityError(DecryptionError): pass  # bad password or tampering

# ========= Format constants =========
MAGIC = b"PWENC"
VER   = 1  # header layout version

# ========= Implementations =========
def _kdf_scrypt(password: str, salt: bytes, *, n_log2=14, r=8, p=1, key_len=32) -> bytes:
    if n_log2 < 10:
        raise EncryptionError(f"scrypt n_log2 too small (got {n_log2}, min 10)")
    return Scrypt(salt=salt, length=key_len, n=1 << n_log2, r=r, p=p).derive(password.encode())

def _cipher_aes_gcm_encrypt(key: bytes, *, nonce_len=12, tag_len=16, data: bytes) -> Tuple[bytes, bytes, bytes]:
    if nonce_len < 12 or tag_len < 12:
        raise EncryptionError(f"AES-GCM params too small (nonce_len={nonce_len}, tag_len={tag_len})")
    nonce = os.urandom(nonce_len)
    enc = Cipher(algorithms.AES(key), modes.GCM(nonce, min_tag_length=tag_len)).encryptor()
    ct = enc.update(data) + enc.finalize()
    return nonce, ct, enc.tag  # tag length enforced by backend

def _cipher_aes_gcm_decrypt(key: bytes, *, nonce: bytes, tag: bytes, data: bytes) -> bytes:
    dec = Cipher(algorithms.AES(key), modes.GCM(nonce)).decryptor()
    return dec.update(data) + dec.finalize_with_tag(tag)

# ========= Profiles (callables embedded) =========
KDF_PROFILES: Dict[str, Dict[str, Any]] = {
    "rp_2025": {
        "fn": _kdf_scrypt,  # direct callable
        "kwargs": {"n_log2": 14, "r": 8, "p": 1, "key_len": 32, "salt_len": 16},
    },
    # add legacy or future profiles here (e.g., "rp_2027": {...})
}

CIPHER_PROFILES: Dict[str, Dict[str, Any]] = {
    "rp_2025": {
        "encrypt_fn": _cipher_aes_gcm_encrypt,  # direct callable
        "decrypt_fn": _cipher_aes_gcm_decrypt,  # direct callable
        "kwargs": {"nonce_len": 12, "tag_len": 16},
    },
    # add legacy or future profiles here
}

# ========= API =========
def encrypt_bytes_with_password(
    data: bytes,
    password: str,
    *,
    kdf: str = "rp_2025",
    cipher: str = "rp_2025",
) -> bytes:
    # Only raise EncryptionError for expected issues; let programming errors surface.
    if kdf not in KDF_PROFILES:
        raise EncryptionError(f"Unknown KDF profile '{kdf}'. Known: {list(KDF_PROFILES)}")
    if cipher not in CIPHER_PROFILES:
        raise EncryptionError(f"Unknown cipher profile '{cipher}'. Known: {list(CIPHER_PROFILES)}")

    kdf_meta  = KDF_PROFILES[kdf]
    ciph_meta = CIPHER_PROFILES[cipher]

    kdf_fn = kdf_meta.get("fn")
    enc_fn = ciph_meta.get("encrypt_fn")
    if not callable(kdf_fn):
        raise EncryptionError(f"KDF profile '{kdf}' has no callable 'fn'")
    if not callable(enc_fn):
        raise EncryptionError(f"Cipher profile '{cipher}' has no callable 'encrypt_fn'")

    salt_len = int(kdf_meta["kwargs"].get("salt_len", 16))
    if salt_len < 8:
        raise EncryptionError(f"salt_len too small ({salt_len})")
    salt = os.urandom(salt_len)

    key = kdf_fn(password, salt, **{k: v for k, v in kdf_meta["kwargs"].items() if k != "salt_len"})
    nonce, ct, tag = enc_fn(key, **ciph_meta["kwargs"], data=data)

    # Minimal self-describing meta: version + profile names
    meta = {"ver": VER, "kdf_profile": kdf, "cipher_profile": cipher}
    meta_bytes = msgpack.packb(meta, use_bin_type=True)

    return MAGIC + struct.pack(">I", len(meta_bytes)) + meta_bytes + salt + nonce + ct + tag

def decrypt_bytes_with_password(blob: bytes, password: str) -> bytes:
    # Parse header with explicit, contextual errors
    need = len(MAGIC) + 4
    if not blob.startswith(MAGIC) or len(blob) < need:
        got_magic = blob[:len(MAGIC)]
        raise HeaderError(f"Bad magic or truncated blob (expected={MAGIC!r}, got={got_magic!r}, total_len={len(blob)})")

    i = len(MAGIC)
    (mlen,) = struct.unpack_from(">I", blob, i); i += 4
    meta_start, meta_end = i, i + mlen
    if len(blob) < meta_end:
        raise HeaderError(f"Truncated meta header (declared={mlen} bytes, available={len(blob)-meta_start})")

    try:
        meta = msgpack.unpackb(blob[meta_start:meta_end], raw=False)
    except Exception as e:
        raise HeaderError(f"Failed to parse msgpack meta at [{meta_start}:{meta_end}]: {e}") from e

    if meta.get("ver") != VER:
        raise UnsupportedVersion(f"Unsupported version {meta.get('ver')} (supported={VER})")

    kdf_profile    = meta.get("kdf_profile")
    cipher_profile = meta.get("cipher_profile")
    if kdf_profile not in KDF_PROFILES:
        raise UnknownProfile(f"Unknown KDF profile '{kdf_profile}' in blob")
    if cipher_profile not in CIPHER_PROFILES:
        raise UnknownProfile(f"Unknown cipher profile '{cipher_profile}' in blob")

    kdf_meta  = KDF_PROFILES[kdf_profile]
    ciph_meta = CIPHER_PROFILES[cipher_profile]

    kdf_fn  = kdf_meta.get("fn")
    dec_fn  = ciph_meta.get("decrypt_fn")
    if not callable(kdf_fn):
        raise UnknownProfile(f"KDF profile '{kdf_profile}' has no callable 'fn'")
    if not callable(dec_fn):
        raise UnknownProfile(f"Cipher profile '{cipher_profile}' has no callable 'decrypt_fn'")

    salt_len  = int(kdf_meta["kwargs"].get("salt_len", 16))
    nonce_len = int(ciph_meta["kwargs"].get("nonce_len", 12))
    tag_len   = int(ciph_meta["kwargs"].get("tag_len", 16))

    i = meta_end
    min_after = i + salt_len + nonce_len + tag_len
    if len(blob) < min_after:
        raise HeaderError(
            f"Truncated body: need >= {min_after} bytes after header "
            f"(salt={salt_len}, nonce={nonce_len}, tag={tag_len}), total={len(blob)}"
        )

    salt  = blob[i:i+salt_len];  i += salt_len
    nonce = blob[i:i+nonce_len]; i += nonce_len
    ct    = blob[i:-tag_len]
    tag   = blob[-tag_len:]

    key = kdf_fn(password, salt, **{k: v for k, v in kdf_meta["kwargs"].items() if k != "salt_len"})
    try:
        return dec_fn(key, nonce=nonce, tag=tag, data=ct, **{k:v for k, v in ciph_meta["kwargs"].items() if k not in ("nonce_len","tag_len")})
    except CryptoInvalidTag as e:
        raise IntegrityError(
            f"Integrity check failed (profiles: kdf='{kdf_profile}', cipher='{cipher_profile}', "
            f"nonce_len={nonce_len}, tag_len={tag_len}). Wrong password or tampered data."
        ) from e
