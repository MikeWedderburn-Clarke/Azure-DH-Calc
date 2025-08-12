from __future__ import annotations
from typing import Literal
from .pricing_client import query_prices
from .cache import CacheConfig, save_cache


def fetch_dedicated_host_prices(region: str, currency: str, max_items: int | None = None) -> list[dict]:
    # Use productName contains 'Dedicated Host' which empirically returns expected host SKUs
    filt = (
        f"serviceFamily eq 'Compute' and armRegionName eq '{region}' and "
        "priceType eq 'Consumption' and contains(productName,'Dedicated Host')"
    )
    return query_prices(filt, currency_code=currency, page_size=200, max_items=max_items)


def fetch_vm_prices(region: str, currency: str, max_items: int | None = None) -> list[dict]:
    filt = (
        f"serviceFamily eq 'Compute' and armRegionName eq '{region}' and "
        "priceType eq 'Consumption' and serviceName eq 'Virtual Machines'"
    )
    return query_prices(filt, currency_code=currency, page_size=400, max_items=max_items)


def populate_region_prices(
    region: str,
    currency: str,
    cache_cfg: CacheConfig,
    kinds: list[Literal['vms','hosts']] | None = None,
    vm_max: int | None = None,
    host_max: int | None = None,
) -> dict[str, int]:
    kinds = kinds or ["hosts", "vms"]
    counts: dict[str, int] = {}
    if "hosts" in kinds:
        host_items = fetch_dedicated_host_prices(region, currency, max_items=host_max)
        save_cache(cache_cfg, region, "hosts", host_items)
        counts["hosts"] = len(host_items)
    if "vms" in kinds:
        vm_items = fetch_vm_prices(region, currency, max_items=vm_max)
        save_cache(cache_cfg, region, "vms", vm_items)
        counts["vms"] = len(vm_items)
    return counts
