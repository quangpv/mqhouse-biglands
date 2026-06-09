"""
Biglands.vn GraphQL Data Crawler

Crawls all product data from the Biglands GraphQL API and saves to data/.
Steps:
1. Count products (CountProductByStatus)
2. Paginate through all products (GetListProductsForSearch)
3. Fetch individual product details (GetProductForClient)

Usage:
  python crawler.py [--token TOKEN] [--no-details] [--limit N]
"""

import os
import sys
import json
import time
import argparse
import logging
import threading
import concurrent.futures
from pathlib import Path
from typing import Optional

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

API_URL = "https://api.biglands.vn/v1/graphql"
DATA_DIR = Path("data")
PAGE_SIZE = 20
REQUEST_DELAY = 0.3
MAX_RETRIES = 3

DEFAULT_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImJhM2MxNjA2Y2ZiNjkzNWRlNGJkYTg3YzI1NzE2ZmM1Y2FiYzU4ZDMiLCJ0eXAiOiJKV1QifQ.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidXNlciIsImFkbWluIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InVzZXIiLCJ4LWhhc3VyYS11c2VyLWlkIjoiZjhkMDI0YjUtMzU5OC00ZmIwLTg2OTEtZTljMmI3NzIyNjEyIn19.Pn7iLN2TbYqR9J_kYEQJdA5z_5Kh_Vz3NHtNPMwQWQRFdOYHbkTb04c0Ipc9XrYQJmTSq1gRbqVBvy0Bgtqnpz3h5ZfoGBL3p7q5o2tTG27iY4vRMH3pspqfVW9k_YaQr7FB0FQ4Jq7Nf0vEJAjbAtRXK8MCQIPhCQmI0rQ5aA-1HNvKfpQHYB6Gj2Y1nV5eG46_dgDp3c6LJR_DP2SfmFy5jhVVOkZQ0hPKJOH38v9IGj3hCDixFNbXvTFK87Efyn0mg79xER6I5_Ap_Q0a5m6O8sfJwZqGphn5J5cpYh5JIPST6TZAT4K2FsPG4D4aQsDp1dY4Br5YxYIBWQ"


def make_query(query_name: str, query_str: str, variables: dict, token: str) -> Optional[dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "operationName": query_name,
        "query": query_str,
        "variables": variables,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
            if resp.status_code == 429:
                wait = 2 ** attempt
                log.warning("Rate limited, waiting %ds...", wait)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            if "errors" in data:
                log.error("GraphQL errors in %s: %s", query_name, data["errors"])
                return None
            return data["data"]
        except requests.RequestException as e:
            log.warning("Attempt %d/%d failed for %s: %s", attempt, MAX_RETRIES, query_name, e)
            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
    return None


# ---- GraphQL Queries ----

COUNT_QUERY = """
query CountProductByStatus($where: products_bool_exp) {
  products_aggregate(where: $where) {
    aggregate {
      count
    }
  }
}
"""

# All 25 product type IDs from the frontend
ALL_TYPE_IDS = [
    "2c1afbdb-86ab-45b6-a157-ea7d48941fc9", "2c8f6dac-257b-46df-96c9-d45f5c8ffa9e",
    "316cd7a1-b544-46e5-8507-1f28cf458476", "36cb352a-822a-48f1-9ae7-a74e0ccdf4ff",
    "43b802d4-ec50-4ed5-9bde-fe8649685cd7", "48cc54de-e089-40fa-b07c-922870167be5",
    "5e9fc932-43b9-416b-bfd5-9f05f282ba95", "60e8a820-eb6c-4e6a-909c-68c81c5d2250",
    "6661fbc7-e911-4dd1-969a-8c3ab69395fb", "966c1acb-3200-47b8-a21d-6a1949333d74",
    "a17883fd-16aa-40c2-850d-d433b8374f14", "ba6ad806-0a8b-4573-b177-f241f2f473b9",
    "c03e6b63-330e-42ae-9356-a77b38ac37dd", "c40c7f5f-26a8-4690-bf07-c2ce58bd7552",
    "e2bbbb7c-0980-4543-b4e5-f9a27b0d979d", "eba629a8-67b4-4471-a2b3-6afb0f2299e8",
    "ef87168e-4f5b-493c-8521-3640ebbefc01", "dccf9c18-1af4-4c75-9fbc-7200e42d865b",
    "82b0502c-3180-412b-ad54-68c651dd9306", "32eddcf9-4168-4379-b188-43e8e064690a",
    "8fcf525f-ecea-45bf-bcb2-a6f2bd79de0e", "f0e02859-60a1-4bab-899d-100ab500f5cc",
    "c9b4eeab-8c18-4850-b950-f23fccca8cba", "867f3264-7c01-41f9-9012-b35cb29f64dd",
    "c22a1372-2d46-4d39-97e0-28d4bb59a775",
]

LIST_QUERY = """
query GetListProductsForSearch($where: products_bool_exp!, $orderBy: [products_order_by!], $limit: Int!, $offset: Int!) {
  products(where: $where, limit: $limit, offset: $offset, order_by: $orderBy) {
    commission
    commission_unit
    price
    price_status
    created_at
    updated_at
    last_approve_at
    quantity_room
    quantity_toilet
    quantity_floor
    images
    status
    id
    title
    owner_name
    owner_id
    current_order_session_id
    current_update_id
    product_approve_orders {
      approve_type
      id
    }
    product_form {
      name
      id
    }
    ward_id
    distance_alley_to_house
    area
    full_address
    short_address
    product_width
    product_length
    tags
    product_hots(limit: 1, order_by: {updated_at: desc}) {
      id
      start_at
      end_at
      priority
      product_id
      created_at
      updated_at
    }
  }
  products_aggregate(where: $where, order_by: $orderBy) {
    aggregate {
      count(distinct: true)
    }
  }
}
"""

USERS_QUERY = """
query GetListUsersForSearch($input: users_bool_exp!, $orderBy: [users_order_by!], $limit: Int!, $offset: Int!) {
  users(where: $input, limit: $limit, offset: $offset, order_by: $orderBy) {
    id
    created_at
    name
    avatar
    current_location
    phone_number
    email
    allow_all_device
    allow_device_id
    blocked_at
    user_roles {
      role_id
    }
    username_passwords {
      username
    }
  }
  users_aggregate(where: $input, order_by: $orderBy) {
    aggregate {
      count(distinct: true)
    }
  }
}
"""

USER_ROLE_FILTER = ["mqhouse", "mqland", "idland", "myland"]

DETAIL_QUERY = """
query GetProductForClient($productId: String!) {
  products_by_pk(id: $productId) {
    id
    title
    price
    commission
    commission_unit
    price_status
    area
    product_width
    product_length
    quantity_room
    quantity_toilet
    quantity_floor
    images
    status
    owner_name
    owner_id
    owner_phone_number
    full_address
    short_address
    ward_id
    distance_alley_to_house
    direction
    legal_record
    tags
    videos
    code
    description
    created_at
    updated_at
    current_order_session_id
    product_order_session {
      current_progress
      user_id
    }
    product_form {
      name
      id
    }
    product_place {
      name
      id
    }
    product_type {
      name
      id
    }
    product_hots(limit: 1, order_by: {updated_at: desc}) {
      id
      start_at
      end_at
      priority
      product_id
      created_at
      updated_at
    }
  }
}
"""


def make_listing_where() -> dict:
    return {
        "_and": [
            {"product_type_id": {"_in": ALL_TYPE_IDS}},
            {"status": {"_in": ["available", "deposited", "sold"]}},
        ]
    }


def count_products(token: str) -> int:
    data = make_query("CountProductByStatus", COUNT_QUERY, {}, token)
    if data:
        count = data["products_aggregate"]["aggregate"]["count"]
        log.info("Total products: %d", count)
        return count
    return 0


def crawl_listing(token: str) -> list[str]:
    all_ids = []
    offset = 0
    total_saved = 0
    listing_file = DATA_DIR / "products.jsonl"

    while True:
        variables = {
            "where": make_listing_where(),
            "orderBy": [{"last_approve_at": "desc"}],
            "limit": PAGE_SIZE,
            "offset": offset,
        }
        data = make_query("GetListProductsForSearch", LIST_QUERY, variables, token)
        if not data:
            log.error("Failed to fetch page at offset %d, stopping", offset)
            break

        products = data.get("products", [])
        if not products:
            log.info("No more products at offset %d, done.", offset)
            break

        with open(listing_file, "a") as f:
            for p in products:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
                all_ids.append(p["id"])

        total_saved += len(products)
        agg = data.get("products_aggregate", {}).get("aggregate", {})
        total_count = agg.get("count", 0)
        log.info(
            "Page at offset %d: saved %d products (total: %d, db: %d)",
            offset, len(products), total_saved, total_count,
        )

        if len(products) < PAGE_SIZE:
            log.info("Last page reached.")
            break

        offset += PAGE_SIZE
        time.sleep(REQUEST_DELAY)

    log.info("Listing done: %d products saved to %s", total_saved, listing_file)
    return all_ids


def crawl_details(product_ids: list[str], token: str, workers: int = 8):
    detail_file = DATA_DIR / "product_details.jsonl"
    write_lock = threading.Lock()
    counter_lock = threading.Lock()
    saved = 0
    errors = 0
    completed = 0

    already_done: set[str] = set()
    if detail_file.exists():
        with open(detail_file) as f:
            for line in f:
                try:
                    already_done.add(json.loads(line)["id"])
                except (json.JSONDecodeError, KeyError):
                    pass
        log.info("Skipping %d already-fetched details", len(already_done))

    pending = [pid for pid in product_ids if pid not in already_done]
    total = len(pending)
    log.info("Fetching details for %d products (%d workers)...", total, workers)

    def fetch_one(pid: str):
        nonlocal saved, errors, completed
        data = make_query("GetProductForClient", DETAIL_QUERY, {"productId": pid}, token)
        with counter_lock:
            if data and data.get("products_by_pk"):
                with write_lock:
                    with open(detail_file, "a") as f:
                        f.write(json.dumps(data["products_by_pk"], ensure_ascii=False) + "\n")
                saved += 1
            else:
                errors += 1
            completed += 1
            if completed % 50 == 0:
                log.info("Details: %d/%d (saved: %d, errors: %d)", completed, total, saved, errors)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(fetch_one, pending)

    log.info("Details done: %d saved, %d errors out of %d", saved, errors, total)


def save_token(token: str):
    token_file = DATA_DIR / "token.txt"
    with open(token_file, "w") as f:
        f.write(token)
    log.info("Token saved to %s", token_file)


def crawl_users(token: str):
    out_file = "data/users.jsonl"
    offset = 0
    page_size = 50
    total = None
    crawled = 0

    # resume: count existing lines
    if os.path.exists(out_file):
        with open(out_file) as f:
            for crawled, _ in enumerate(f, 1):
                pass
        offset = crawled
        log.info("Resuming users crawl at offset %d", offset)

    while total is None or offset < total:
        variables = {
            "input": {"user_roles": {"role_id": {"_in": USER_ROLE_FILTER}}},
            "orderBy": [{"created_at": "desc"}],
            "limit": page_size,
            "offset": offset,
        }
        data = make_query("GetListUsersForSearch", USERS_QUERY, variables, token)
        if data is None:
            log.error("Failed to fetch users, aborting")
            break
        users = data.get("users", [])
        agg = data.get("users_aggregate", {})
        total = agg.get("aggregate", {}).get("count", 0)
        if not users:
            break

        with open(out_file, "a") as f:
            for u in users:
                f.write(json.dumps(u, ensure_ascii=False) + "\n")
        crawled += len(users)
        offset += page_size
        log.info("Users: %d/%d", crawled, total)
    log.info("Users crawl complete: %d users → %s", crawled, out_file)


def main():
    parser = argparse.ArgumentParser(description="Biglands GraphQL Data Crawler")
    parser.add_argument("--token", help="Bearer token (default: embedded demo token)")
    parser.add_argument("--no-details", action="store_true", help="Skip individual product detail crawling")
    parser.add_argument("--limit", type=int, default=0, help="Max products to crawl (0 = all)")
    parser.add_argument("--resume", action="store_true", help="Skip listing if products.jsonl already exists")
    parser.add_argument("--workers", type=int, default=8, help="Parallel workers for detail fetching")
    parser.add_argument("--users", action="store_true", help="Crawl users instead of products")
    args = parser.parse_args()

    token = args.token or os.environ.get("BEARER_TOKEN") or DEFAULT_TOKEN
    DATA_DIR.mkdir(exist_ok=True)
    save_token(token)

    if args.users:
        crawl_users(token)
        return

    listing_file = DATA_DIR / "products.jsonl"
    if args.resume and listing_file.exists():
        log.info("Resume mode: loading product IDs from existing listing...")
        with open(listing_file) as f:
            product_ids = [json.loads(line)["id"] for line in f]
        log.info("Loaded %d product IDs from %s", len(product_ids), listing_file)
    else:
        total = count_products(token)
        if total == 0:
            log.error("No products found or API returned errors. Token may be expired.")
            sys.exit(1)
        product_ids = crawl_listing(token)

    if args.limit > 0:
        product_ids = product_ids[:args.limit]
        log.info("Limited to %d products for detail crawl", len(product_ids))

    if not args.no_details and product_ids:
        crawl_details(product_ids, token, workers=args.workers)
    elif not args.no_details:
        log.warning("No product IDs to fetch details for.")
    else:
        log.info("Detail crawling skipped (--no-details).")

    listing_count = 0
    listing_file = DATA_DIR / "products.jsonl"
    if listing_file.exists():
        with open(listing_file) as f:
            listing_count = sum(1 for _ in f)

    detail_count = 0
    detail_file = DATA_DIR / "product_details.jsonl"
    if detail_file.exists():
        with open(detail_file) as f:
            detail_count = sum(1 for _ in f)

    log.info("=" * 50)
    log.info("Crawl complete!")
    log.info("  Listing:  %d products -> data/products.jsonl", listing_count)
    log.info("  Details:  %d products -> data/product_details.jsonl", detail_count)
    log.info("=" * 50)


if __name__ == "__main__":
    main()
