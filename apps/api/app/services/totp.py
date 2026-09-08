"""RFC 6238 TOTP + hashed backup codes. No extra dependency."""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import struct
import time
import urllib.parse


def new_secret() -> str:
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii").rstrip("=")


def _key(secret: str) -> bytes:
    padded = secret.upper() + "=" * ((8 - len(secret) % 8) % 8)
    return base64.b32decode(padded, casefold=True)


def hotp(secret: str, counter: int, digits: int = 6) -> str:
    digest = hmac.new(_key(secret), struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    number = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
    return str(number % (10**digits)).zfill(digits)


def verify_code(secret: str, code: str, window: int = 1) -> bool:
    digits = "".join(ch for ch in (code or "") if ch.isdigit())
    if not secret or len(digits) != 6:
        return False
    counter = int(time.time() // 30)
    for delta in range(-window, window + 1):
        if hmac.compare_digest(hotp(secret, counter + delta), digits):
            return True
    return False


def otpauth_uri(secret: str, email: str) -> str:
    label = urllib.parse.quote(f"SHC:{email}")
    query = urllib.parse.urlencode(
        {"secret": secret, "issuer": "SHC", "algorithm": "SHA1", "digits": 6, "period": 30}
    )
    return f"otpauth://totp/{label}?{query}"


def hash_backup(code: str) -> str:
    return hashlib.sha256(code.strip().lower().encode("utf-8")).hexdigest()


def new_backup_codes(count: int = 8) -> list[str]:
    return [secrets.token_hex(4) for _ in range(count)]


def parse_backup_hashes(blob: str) -> list[str]:
    return [part for part in (blob or "").split(",") if part]


def consume_backup(blob: str, code: str) -> str | None:
    digest = hash_backup(code)
    hashes = parse_backup_hashes(blob)
    kept: list[str] = []
    used = False
    for item in hashes:
        if not used and hmac.compare_digest(item, digest):
            used = True
            continue
        kept.append(item)
    return ",".join(kept) if used else None
