from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .vm_catalog import get_vm_size
from .host_catalog import list_host_types
from .models import HostPlanOption


@dataclass(frozen=True)
class Requirement:
    vcpus: int
    memory_gib: float


def requirement_from_vm(sku: str, count: int) -> Requirement:
    vm = get_vm_size(sku)
    return Requirement(vcpus=vm.vcpus * count, memory_gib=vm.memory_gib * count)


def plan_options(req: Requirement) -> list[HostPlanOption]:
    options: list[HostPlanOption] = []
    for host_type in list_host_types():
        hosts_needed = host_type.hosts_needed(req.vcpus, req.memory_gib)
        options.append(HostPlanOption(host_type=host_type, host_count=hosts_needed))
    options.sort(key=lambda o: o.total_monthly_cost)
    return options


def summarize(req: Requirement, options: Iterable[HostPlanOption]) -> list[dict]:
    summary: list[dict] = []
    for opt in options:
        summary.append(
            {
                "host_type": opt.host_type.name,
                "hosts": opt.host_count,
                "total_vcpus": opt.total_vcpus,
                "total_mem_gib": opt.total_memory_gib,
                "monthly_cost": round(opt.total_monthly_cost, 2),
                "cost_per_vcpu": round(opt.total_monthly_cost / req.vcpus, 2) if req.vcpus else 0,
            }
        )
    return summary
