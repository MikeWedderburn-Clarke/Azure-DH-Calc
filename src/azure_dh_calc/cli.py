from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from .calculator import requirement_from_vm, plan_options, summarize
from .cache import CacheConfig, list_cached_regions, load_cache
from .price_cache_populator import populate_region_prices

app = typer.Typer(help="Azure Dedicated Hosts calculator (MVP)")
console = Console()


@app.command("calc")
def calc_command(
    region: str = typer.Option(..., "--region", "-r", help="Azure region, e.g. westeurope"),
    currency: str = typer.Option(..., "--currency", "-c", help="Currency code, e.g. USD"),
    vm_sku: str = typer.Option(..., "--vm-sku", "-s", help="Azure VM size SKU, e.g. D2s_v3"),
    count: int = typer.Option(..., "--count", "-n", min=1, help="Number of VM instances"),
):
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


@app.command("cache-refresh")
def cache_refresh(
    region: str = typer.Option(..., "--region", "-r"),
    currency: str = typer.Option("USD", "--currency", "-c"),
    base_dir: Path = typer.Option(Path("data/cache"), "--cache-dir", exists=False, file_okay=False),
    kinds: list[str] = typer.Option(["hosts", "vms"], "--kind", help="Kinds to refresh: hosts, vms"),
    ttl: int = typer.Option(24 * 3600, "--ttl", help="TTL seconds stored in metadata"),
    vm_max: int | None = typer.Option(None, "--vm-max", help="Optional max VM price records (for quicker dev runs)"),
    host_max: int | None = typer.Option(None, "--host-max", help="Optional max host price records"),
):
    cfg = CacheConfig(base_dir=base_dir, ttl_seconds=ttl)
    try:
        counts = populate_region_prices(
            region,
            currency,
            cfg,
            kinds=[k for k in kinds],
            vm_max=vm_max,
            host_max=host_max,
        )
    except Exception as e:  # pragma: no cover
        console.print(f"[red]Failed to refresh cache: {e}[/red]")
        raise typer.Exit(1)
    console.print({"region": region, "counts": counts, "dir": str(cfg.region_dir(region))})


@app.command("cache-list")
def cache_list(base_dir: Path = typer.Option(Path("data/cache"), "--cache-dir")):
    cfg = CacheConfig(base_dir=base_dir)
    regions = list_cached_regions(cfg)
    table = Table(title="Cached Regions")
    table.add_column("Region")
    table.add_column("VMs")
    table.add_column("Hosts")
    for r in regions:
        vm = cfg.file_path(r, "vms").exists()
        host = cfg.file_path(r, "hosts").exists()
        table.add_row(r, "yes" if vm else "no", "yes" if host else "no")
    console.print(table)


@app.command("cache-show")
def cache_show(
    region: str = typer.Option(..., "--region", "-r"),
    kind: str = typer.Option("hosts", "--kind"),
    base_dir: Path = typer.Option(Path("data/cache"), "--cache-dir"),
    limit: int = typer.Option(5, "--limit"),
):
    cfg = CacheConfig(base_dir=base_dir)
    data = load_cache(cfg, region, kind)  # type: ignore[arg-type]
    if not data:
        console.print(f"[yellow]No cache for {region} {kind}[/yellow]")
        raise typer.Exit(1)
    items = data.get("items", [])[:limit]
    console.print({k: data[k] for k in ["_region", "_kind", "count"] if k in data})
    console.print(items)


def main():  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
