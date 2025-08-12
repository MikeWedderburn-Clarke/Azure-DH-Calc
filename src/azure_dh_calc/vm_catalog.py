"""Static starter VM catalog.

Real implementation will query Azure or load from cached JSON.
"""
from __future__ import annotations
from .models import VMSize

VM_SIZES: dict[str, VMSize] = {
    # (Representative subset) - approximate memory numbers
    "D2s_v3": VMSize("D2s_v3", vcpus=2, memory_gib=8),
    "D4s_v3": VMSize("D4s_v3", vcpus=4, memory_gib=16),
    "D8s_v3": VMSize("D8s_v3", vcpus=8, memory_gib=32),
    "E2s_v5": VMSize("E2s_v5", vcpus=2, memory_gib=16),
    "E4s_v5": VMSize("E4s_v5", vcpus=4, memory_gib=32),
    "E8s_v5": VMSize("E8s_v5", vcpus=8, memory_gib=64),
}


def get_vm_size(sku: str) -> VMSize:
    try:
        return VM_SIZES[sku]
    except KeyError as exc:
        raise ValueError(f"Unknown VM SKU '{sku}'. Extend VM_SIZES or implement dynamic lookup.") from exc
