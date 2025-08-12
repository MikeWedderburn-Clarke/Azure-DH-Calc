"""Azure Retail Prices API client with simple pagination.

The public Prices API returns pages of results with a `NextPageLink` when more data
is available. We iterate until exhausted or an optional ``max_items`` limit is
reached. ``page_size`` controls the ``$top`` (page size) for the first request
only (subsequent `NextPageLink` URLs already encode their paging state and must
be called without query params).
"""
from __future__ import annotations
from typing import Optional
import requests

BASE_URL = "https://prices.azure.com/api/retail/prices"


def query_prices(
    filter_expr: str,
    currency_code: str | None = None,
    page_size: int = 200,
    max_items: Optional[int] = None,
) -> list[dict]:
    """Return list of price records for filter expression.

    Parameters
    ----------
    filter_expr: OData filter for the Prices API.
    currency_code: Optional ISO currency code (e.g. USD, EUR).
    page_size: ``$top`` for the first request (subsequent pages follow server defaults).
    max_items: Optional hard cap to stop early (useful for tests).
    """
    params = {"$filter": filter_expr, "$top": page_size}
    if currency_code:
        params["currencyCode"] = currency_code
    results: list[dict] = []
    next_url: str | None = BASE_URL
    while next_url:
        resp = requests.get(next_url, params=params if next_url == BASE_URL else None, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("Items", [])
        if not isinstance(items, list):  # defensive
            break
        results.extend(items)
        if max_items and len(results) >= max_items:
            return results[:max_items]
        next_url = data.get("NextPageLink")
    return results
