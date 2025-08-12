from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Any
import time

CacheKind = Literal["vms", "hosts"]


@dataclass(frozen=True)
class CacheConfig:
    base_dir: Path
    ttl_seconds: int = 24 * 3600  # default 24h

    def region_dir(self, region: str) -> Path:
        return self.base_dir / region.lower()

    def file_path(self, region: str, kind: CacheKind) -> Path:
        return self.region_dir(region) / f"{kind}.json"


def load_cache(config: CacheConfig, region: str, kind: CacheKind) -> dict[str, Any] | None:
    path = config.file_path(region, kind)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        ts = payload.get("_fetched_at")
        if ts and (time.time() - ts > config.ttl_seconds):
            return None  # stale
        return payload
    except Exception:
        return None


def save_cache(config: CacheConfig, region: str, kind: CacheKind, items: list[dict[str, Any]]) -> None:
    region_path = config.region_dir(region)
    region_path.mkdir(parents=True, exist_ok=True)
    path = config.file_path(region, kind)
    payload = {
        "_region": region.lower(),
        "_kind": kind,
        "_fetched_at": time.time(),
        "count": len(items),
        "items": items,
    }
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    tmp.replace(path)


def list_cached_regions(config: CacheConfig) -> list[str]:
    if not config.base_dir.exists():
        return []
    return sorted([p.name for p in config.base_dir.iterdir() if p.is_dir()])
