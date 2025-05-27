import pytest
import httpx

BASE_URL = "http://localhost:8000"  

TEST_USER = {
    "email": "string",
    "password": "string"
}


test_cases = [
    # Easy
    {
        "query": "I want a food tour in Paris",
        "expected_ids": [2]
    },
    # Medium
    {
        "query": "Looking for a family-friendly fantasy tour in London",
        "expected_ids": [4]
    },
    {
        "query": "Something romantic in Italy",
        "expected_ids": [9, 8]
    },
    # Hard
    {
        "query": "Adventure in nature but no overnight stay",
        "expected_ids": [0, 6, 7]
    },
    
]

def login_and_get_token():
    response = httpx.post(f"{BASE_URL}/auth/login", json=TEST_USER)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access"]

@pytest.fixture(scope="module")
def auth_headers():
    token = login_and_get_token()
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.parametrize("query,expected_ids", [(case["query"], case["expected_ids"]) for case in test_cases])
def test_recommendation_precision(query, expected_ids, auth_headers):
    response = httpx.post(
        f"{BASE_URL}/recommendations/",
        headers=auth_headers,
        json={"prompt": query},
        timeout=60.0 
    )
    assert response.status_code == 200, f"Request failed: {response.status_code} – {query}"

    data = response.json()
    returned_ids = [activity['id'] for activity in data]
    top_k = returned_ids[:3]

    matched = set(expected_ids) & set(top_k)
    precision = len(matched) / min(3, len(top_k)) if top_k else 0

    print(f"\n🔍 Query: {query}")
    print(f"✅ Expected IDs: {expected_ids}")
    print(f"📦 Returned IDs: {returned_ids}")

    assert precision > 0, f"No relevant results returned for: {query}"
