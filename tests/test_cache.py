from pathlib import Path
from azure_dh_calc.cache import CacheConfig, save_cache, load_cache, list_cached_regions

def test_round_trip_cache(tmp_path: Path):
    cfg = CacheConfig(base_dir=tmp_path, ttl_seconds=60)
    region = "westeurope"
    items = [{"sku": "D2s_v3", "price": 0.1}]
    save_cache(cfg, region, "vms", items)
    loaded = load_cache(cfg, region, "vms")
    assert loaded is not None
    assert loaded["count"] == 1
    assert loaded["items"][0]["sku"] == "D2s_v3"
    assert region in list_cached_regions(cfg)

def test_ttl_expiry(tmp_path: Path):
    cfg = CacheConfig(base_dir=tmp_path, ttl_seconds=0)
    save_cache(cfg, "westeurope", "hosts", [{"name": "DSv3-Type1"}])
    # Immediate load should treat as stale because ttl=0
    assert load_cache(cfg, "westeurope", "hosts") is None
