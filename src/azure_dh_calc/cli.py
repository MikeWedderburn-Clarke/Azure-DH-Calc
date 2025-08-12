from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from .calculator import requirement_from_vm, plan_options, summarize

app = typer.Typer(help="Azure Dedicated Hosts calculator (MVP)")
console = Console()


@app.command()
def calc(region: str, currency: str, vm_sku: str, count: int = typer.Argument(..., min=1)):
    """Calculate dedicated host options for N instances of a VM SKU."""
    # Region & currency presently unused in static MVP - placeholder for future pricing lookup.
    req = requirement_from_vm(vm_sku, count)
    options = plan_options(req)
    rows = summarize(req, options)
    table = Table(title=f"Dedicated Host Options for {count} x {vm_sku} ({req.vcpus} vCPU / {req.memory_gib} GiB)")
    table.add_column("Host Type")
    table.add_column("# Hosts", justify="right")
    table.add_column("Total vCPUs", justify="right")
    table.add_column("Total Mem (GiB)", justify="right")
    table.add_column("Monthly Cost", justify="right")
    table.add_column("Cost / vCPU", justify="right")
    for r in rows:
        table.add_row(
            r["host_type"],
            str(r["hosts"]),
            str(r["total_vcpus"]),
            f"{r['total_mem_gib']:.0f}",
            f"${r['monthly_cost']:,}",
            f"${r['cost_per_vcpu']}",
        )
    console.print(table)


def main():  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
