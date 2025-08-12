from __future__ import annotations
from typing import Literal
from .pricing_client import query_prices
from .cache import CacheConfig, save_cache


def fetch_dedicated_host_prices(region: str, currency: str, page_size: int = 1000) -> list[dict]:
    filt = (
        f"serviceFamily eq 'Compute' and armRegionName eq '{region}' and "
        "priceType eq 'Consumption' and contains(meterName,'Dedicated Host')"
    )
    return query_prices(filt, currency_code=currency, page_size=page_size)


def fetch_vm_prices(region: str, currency: str, page_size: int = 1000) -> list[dict]:
    filt = (
        f"serviceFamily eq 'Compute' and armRegionName eq '{region}' and "
        "priceType eq 'Consumption' and serviceName eq 'Virtual Machines'"
    )
    return query_prices(filt, currency_code=currency, page_size=page_size)


def populate_region_prices(
    region: str,
    currency: str,
    cache_cfg: CacheConfig,
    kinds: list[Literal['vms','hosts']] | None = None,
    vm_page_size: int = 500,
    host_page_size: int = 200,
) -> dict[str, int]:
    kinds = kinds or ["hosts", "vms"]
    counts: dict[str, int] = {}
    if "hosts" in kinds:
        host_items = fetch_dedicated_host_prices(region, currency, page_size=host_page_size)
        save_cache(cache_cfg, region, "hosts", host_items)
        counts["hosts"] = len(host_items)
    if "vms" in kinds:
        vm_items = fetch_vm_prices(region, currency, page_size=vm_page_size)
        save_cache(cache_cfg, region, "vms", vm_items)
        counts["vms"] = len(vm_items)
    return counts
