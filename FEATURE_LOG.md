## Feature Log

### 0.1.2 - Region Cache Start
- Introduced cache module storing per-region JSON files for VM (vms.json) and Dedicated Host (hosts.json) price/shape data with TTL.

### 0.1.1 - CLI Fix
- Converted CLI to single command with explicit options (-r, -c, -s, -n) to resolve positional parsing issue.
- Updated README usage example.

### 0.1.0 - MVP
- Dev container setup (Python 3.12).
- Static VM & Dedicated Host catalogs.
- Capacity & simple cost calculation (single host type options, homogeneous only).
- CLI command `azure-dh-calc calc`.
- Basic unit test for option ordering & capacity sufficiency.
- CI workflow (lint + tests).

### Planned Next Iterations
- Fetch real Dedicated Host prices via Azure Retail Prices API with region & currency filters.
- Local JSON cache per region (TTL + manual refresh command).
- Mixed host-type packing heuristic (greedy + improvement loop).
- Add REST API (FastAPI) + simple frontend (Static Web App) calling minimal backend (Function).
- Cost normalization & currency conversion using latest FX rates (ECB / Azure built-in if exposed).
- Support reserved vs pay-as-you-go pricing scenarios.
- Output to CSV / JSON.
- Performance profiling & concurrency for price fetches.
