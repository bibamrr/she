from __future__ import annotations

import re
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

_UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
}

_CACHE_DIR = Path("data/logos")
_MEM: dict[str, tuple[float, bytes, str]] = {}
_LOCK = threading.Lock()
_TTL = 7 * 24 * 3600
_MAX_BYTES = 350_000


def _venue(symbol: str) -> str:
    raw = (symbol or "").upper()
    if "/" in raw:
        return "crypto"
    if raw.endswith("=F"):
        return "commodities"
    if raw.endswith(".SR") or raw.replace(".SR", "").isdigit():
        return "tadawul"
    if raw.endswith((".L", ".PA", ".DE", ".AS", ".MI", ".SW", ".MC")):
        return "europe"
    if raw.endswith((".T", ".HK", ".KS", ".KQ", ".SS", ".SZ", ".AX", ".TW", ".NS", ".BO")):
        return "asia"
    return "us"


def _ticker(symbol: str) -> str:
    raw = (symbol or "").strip()
    if "/" in raw:
        return raw.split("/", 1)[0].upper()
    return re.sub(r"\.SR$", "", raw, flags=re.I).upper()


def candidates(symbol: str) -> list[str]:
    venue = _venue(symbol)
    key = _ticker(symbol)
    if not key:
        return []
    low = key.lower()
    if venue == "crypto":
        return [
            f"https://cdn.jsdelivr.net/gh/spothq/cryptocurrency-icons@master/svg/color/{low}.svg",
            f"https://assets.coincap.io/assets/icons/{low}@2x.png",
        ]
    listed = f"{key}.SR" if venue == "tadawul" else key
    urls = [
        f"https://financialmodelingprep.com/image-stock/{listed}.png",
        f"https://assets.parqet.com/logos/symbol/{listed}?format=png",
    ]
    if venue == "us":
        urls.append(f"https://storage.googleapis.com/iex/api/logos/{key}.png")
    return urls


def _safe_name(symbol: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", symbol.upper())[:48]


def _disk_paths(symbol: str) -> tuple[Path, Path]:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    stem = _CACHE_DIR / _safe_name(symbol)
    return stem.with_suffix(".bin"), stem.with_suffix(".type")


def _read_disk(symbol: str) -> Optional[Tuple[bytes, str]]:
    blob, meta = _disk_paths(symbol)
    if not blob.exists() or not meta.exists():
        return None
    if time.time() - blob.stat().st_mtime > _TTL:
        return None
    data = blob.read_bytes()
    ctype = meta.read_text(encoding="utf-8").strip() or "image/png"
    if not data:
        return None
    return data, ctype


def _write_disk(symbol: str, data: bytes, content_type: str) -> None:
    blob, meta = _disk_paths(symbol)
    blob.write_bytes(data)
    meta.write_text(content_type, encoding="utf-8")


def _fetch(url: str) -> Optional[Tuple[bytes, str]]:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=8) as resp:
        ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if not ctype.startswith("image/"):
            return None
        data = resp.read(_MAX_BYTES + 1)
    if not data or len(data) > _MAX_BYTES:
        return None
    return data, ctype


def resolve(symbol: str) -> Optional[Tuple[bytes, str]]:
    key = (symbol or "").strip()
    if not key:
        return None
    now = time.time()
    with _LOCK:
        hit = _MEM.get(key)
        if hit and now - hit[0] < _TTL:
            return hit[1], hit[2]
    disk = _read_disk(key)
    if disk:
        with _LOCK:
            _MEM[key] = (now, disk[0], disk[1])
        return disk
    for url in candidates(key):
        try:
            payload = _fetch(url)
        except (urllib.error.URLError, TimeoutError, ValueError, OSError):
            continue
        if not payload:
            continue
        data, ctype = payload
        with _LOCK:
            _MEM[key] = (now, data, ctype)
            if len(_MEM) > 400:
                _MEM.pop(next(iter(_MEM)), None)
        try:
            _write_disk(key, data, ctype)
        except OSError:
            pass
        return data, ctype
    return None
