"""Static starter Dedicated Host catalog with approximate capacities & placeholder prices.

Prices are illustrative only. Future iteration: fetch real prices from Azure Retail Prices API and cache per region & currency.
"""
from __future__ import annotations
from .models import DedicatedHostType

HOST_TYPES: dict[str, DedicatedHostType] = {
    # name: (family, vcpus, memory_gib, hourly_price)
    "DSv3-Type1": DedicatedHostType("DSv3-Type1", "Dsv3", 64, 256, 4.50),
    "ESv5-Type1": DedicatedHostType("ESv5-Type1", "Esv5", 64, 512, 5.40),
    "FSv2-Type2": DedicatedHostType("FSv2-Type2", "Fsv2", 72, 144, 4.80),
}


def list_host_types() -> list[DedicatedHostType]:
    return list(HOST_TYPES.values())
