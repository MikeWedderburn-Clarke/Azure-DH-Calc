from __future__ import annotations
from dataclasses import dataclass
from math import ceil


@dataclass(frozen=True)
class VMSize:
    sku: str
    vcpus: int
    memory_gib: float


@dataclass(frozen=True)
class DedicatedHostType:
    name: str
    family: str
    vcpus: int
    memory_gib: float
    hourly_price: float  # In chosen currency (assumed already converted)

    @property
    def monthly_price(self) -> float:
        # 730 hour standard approximation
        return self.hourly_price * 730

    def hosts_needed(self, required_vcpus: int, required_memory_gib: float) -> int:
        return max(
            ceil(required_vcpus / self.vcpus),
            ceil(required_memory_gib / self.memory_gib),
        )


@dataclass(frozen=True)
class HostPlanOption:
    host_type: DedicatedHostType
    host_count: int

    @property
    def total_monthly_cost(self) -> float:
        return self.host_type.monthly_price * self.host_count

    @property
    def total_vcpus(self) -> int:
        return self.host_type.vcpus * self.host_count

    @property
    def total_memory_gib(self) -> float:
        return self.host_type.memory_gib * self.host_count
