from __future__ import annotations

import os
import json
import requests

PROJECT_CODE = "reviews-s07"

DEFAULT_ENDPOINT = os.getenv("GRAPHQL_URL", "http://localhost:8189/graphql")


def build_payload(query: str, variables: dict | None = None) -> dict:
    return {
        "query": query,
        "variables": variables or {},
    }


def send(endpoint: str, query: str, variables: dict | None = None) -> dict:
    payload = build_payload(query, variables)
    r = requests.post(endpoint, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


def print_result(result: dict) -> None:
    if "errors" in result and result["errors"]:
        print("GraphQL errors:")
        print(json.dumps(result["errors"], ensure_ascii=False, indent=2))

    if "data" in result and result["data"] is not None:
        print("GraphQL data:")
        print(json.dumps(result["data"], ensure_ascii=False, indent=2))

def main():
    endpoint = DEFAULT_ENDPOINT

    query_reviews = """
    query {
      reviews {
        id
        rating
      }
    }
    """
    print("== Query: reviews ==")
    res1 = send(endpoint, query_reviews, {})
    print_result(res1)

    mutation_create = """
    mutation($rating: Int!) {
      createReview(rating: $rating) {
        id
        rating
      }
    }
    """
    print("\n== Mutation: createReview ==")
    res2 = send(endpoint, mutation_create, {"rating": 5})
    print_result(res2)

if __name__ == "__main__":
    main()
