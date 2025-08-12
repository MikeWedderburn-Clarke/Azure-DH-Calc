"""Azure Retail Prices API client (minimal, optional for later use)."""
from __future__ import annotations
import requests

BASE_URL = "https://prices.azure.com/api/retail/prices"


def query_prices(filter_expr: str, currency_code: str | None = None, page_size: int = 100) -> list[dict]:
    params = {"$filter": filter_expr, "$top": page_size}
    if currency_code:
        params["currencyCode"] = currency_code
    results: list[dict] = []
    next_url: str | None = BASE_URL
    while next_url:
        resp = requests.get(next_url, params=params if next_url == BASE_URL else None, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("Items", [])
        results.extend(items)
        next_url = data.get("NextPageLink")
        if len(results) >= page_size:
            break
    return results
