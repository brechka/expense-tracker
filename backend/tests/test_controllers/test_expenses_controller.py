VALID_PAYLOAD = {"name": "Lunch", "amount": 12.5, "currency": "USD", "category": "Food", "date": "2024-01-15"}


# --- POST /api/expenses/ ---

def test_add_expense(auth_client):
    response = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Lunch"
    assert data["amount"] == 12.5
    assert data["currency"] == "USD"
    assert data["category"] == "Food"
    assert data["date"] == "2024-01-15"


def test_add_expense_missing_fields(auth_client):
    response = auth_client.post("/api/expenses/", json={"name": "Lunch"})
    assert response.status_code == 422


def test_add_expense_empty_name(auth_client):
    response = auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "name": ""})
    assert response.status_code == 422


def test_add_expense_whitespace_name(auth_client):
    response = auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "name": "   "})
    assert response.status_code == 422


def test_add_expense_negative_amount(auth_client):
    response = auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "amount": -1})
    assert response.status_code == 422


def test_add_expense_zero_amount(auth_client):
    response = auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "amount": 0})
    assert response.status_code == 422


def test_add_expense_empty_body(auth_client):
    response = auth_client.post("/api/expenses/", json={})
    assert response.status_code == 422


def test_add_expense_strips_whitespace(auth_client):
    payload = {**VALID_PAYLOAD, "name": "  Lunch  ", "currency": " USD "}
    response = auth_client.post("/api/expenses/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Lunch"
    assert data["currency"] == "USD"


def test_add_expense_unauthenticated(client):
    response = client.post("/api/expenses/", json=VALID_PAYLOAD)
    assert response.status_code == 401


# --- GET /api/expenses/ ---

def test_get_expenses_empty(auth_client):
    response = auth_client.get("/api/expenses/")
    assert response.status_code == 200
    body = response.json()
    assert body["data"] == []
    assert body["total"] == 0
    assert body["limit"] is None
    assert body["offset"] is None


def test_get_expenses_returns_list(auth_client):
    auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "name": "Dinner"})
    response = auth_client.get("/api/expenses/")
    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) == 2
    assert body["total"] == 2


def test_get_expenses_pagination(auth_client):
    for i in range(5):
        auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "name": f"E{i}", "date": f"2024-01-{10+i:02d}"})
    response = auth_client.get("/api/expenses/", params={"limit": 2, "offset": 0})
    body = response.json()
    assert response.status_code == 200
    assert len(body["data"]) == 2
    assert body["total"] == 5
    assert body["limit"] == 2
    assert body["offset"] == 0


def test_get_expenses_pagination_offset(auth_client):
    for i in range(5):
        auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "name": f"E{i}", "date": f"2024-01-{10+i:02d}"})
    response = auth_client.get("/api/expenses/", params={"limit": 2, "offset": 3})
    body = response.json()
    assert len(body["data"]) == 2
    assert body["total"] == 5


def test_get_expenses_limit_zero_invalid(auth_client):
    response = auth_client.get("/api/expenses/", params={"limit": 0})
    assert response.status_code == 422


def test_get_expenses_offset_negative_invalid(auth_client):
    response = auth_client.get("/api/expenses/", params={"offset": -1})
    assert response.status_code == 422


def test_get_expenses_filter_from_date(auth_client):
    auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "date": "2024-01-01"})
    auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "date": "2024-06-01"})
    response = auth_client.get("/api/expenses/", params={"fromDate": "2024-03-01"})
    body = response.json()
    assert len(body["data"]) == 1
    assert body["total"] == 1
    assert body["data"][0]["date"] == "2024-06-01"


def test_get_expenses_filter_to_date(auth_client):
    auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "date": "2024-01-01"})
    auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "date": "2024-06-01"})
    response = auth_client.get("/api/expenses/", params={"toDate": "2024-03-01"})
    body = response.json()
    assert len(body["data"]) == 1
    assert body["total"] == 1
    assert body["data"][0]["date"] == "2024-01-01"


def test_get_expenses_filter_date_range(auth_client):
    auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "date": "2024-01-01"})
    auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "date": "2024-03-15"})
    auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "date": "2024-06-01"})
    response = auth_client.get("/api/expenses/", params={"fromDate": "2024-02-01", "toDate": "2024-05-01"})
    body = response.json()
    assert len(body["data"]) == 1
    assert body["total"] == 1
    assert body["data"][0]["date"] == "2024-03-15"


def test_get_expenses_filter_no_match(auth_client):
    auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    response = auth_client.get("/api/expenses/", params={"fromDate": "2025-01-01"})
    body = response.json()
    assert len(body["data"]) == 0
    assert body["total"] == 0


def test_get_expenses_pagination_with_filter(auth_client):
    for i in range(5):
        auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "name": f"E{i}", "date": f"2024-06-{10+i:02d}"})
    auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "date": "2024-01-01"})
    response = auth_client.get("/api/expenses/", params={"fromDate": "2024-06-01", "limit": 2})
    body = response.json()
    assert len(body["data"]) == 2
    assert body["total"] == 5


# --- GET /api/expenses/{id} ---

def test_get_expense_by_id(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    response = auth_client.get(f"/api/expenses/{expense_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == expense_id
    assert data["name"] == "Lunch"
    assert data["amount"] == 12.5
    assert data["currency"] == "USD"
    assert data["category"] == "Food"
    assert data["date"] == "2024-01-15"


def test_get_expense_by_id_not_found(auth_client):
    response = auth_client.get("/api/expenses/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


# --- PATCH /api/expenses/{id} ---

def test_patch_expense(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    response = auth_client.patch(f"/api/expenses/{expense_id}", json={"name": "Dinner", "amount": 25.0})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Dinner"
    assert data["amount"] == 25.0
    assert data["currency"] == "USD"
    assert data["category"] == "Food"
    assert data["date"] == "2024-01-15"


def test_patch_expense_single_field(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    response = auth_client.patch(f"/api/expenses/{expense_id}", json={"category": "Drinks"})
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Drinks"
    assert data["name"] == "Lunch"
    assert data["amount"] == 12.5


def test_patch_expense_all_fields(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    new_data = {"name": "Dinner", "amount": 99.0, "currency": "EUR", "category": "Drinks", "date": "2025-01-01"}
    response = auth_client.patch(f"/api/expenses/{expense_id}", json=new_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Dinner"
    assert data["amount"] == 99.0
    assert data["currency"] == "EUR"
    assert data["category"] == "Drinks"
    assert data["date"] == "2025-01-01"


def test_patch_expense_not_found(auth_client):
    response = auth_client.patch("/api/expenses/9999", json={"name": "X"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_patch_expense_empty_body(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    response = auth_client.patch(f"/api/expenses/{expense_id}", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "No fields to update"


def test_patch_expense_invalid_amount(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    response = auth_client.patch(f"/api/expenses/{expense_id}", json={"amount": -5})
    assert response.status_code == 422


def test_patch_expense_zero_amount(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    response = auth_client.patch(f"/api/expenses/{expense_id}", json={"amount": 0})
    assert response.status_code == 422


def test_patch_expense_empty_name(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    response = auth_client.patch(f"/api/expenses/{expense_id}", json={"name": ""})
    assert response.status_code == 422


def test_patch_expense_empty_currency(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    response = auth_client.patch(f"/api/expenses/{expense_id}", json={"currency": ""})
    assert response.status_code == 422


def test_patch_expense_persists(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    auth_client.patch(f"/api/expenses/{expense_id}", json={"name": "Updated"})
    get_resp = auth_client.get(f"/api/expenses/{expense_id}")
    assert get_resp.json()["name"] == "Updated"


# --- DELETE /api/expenses/{id} ---

def test_delete_expense(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    response = auth_client.delete(f"/api/expenses/{expense_id}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_expense_then_get_returns_404(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    auth_client.delete(f"/api/expenses/{expense_id}")
    assert auth_client.get(f"/api/expenses/{expense_id}").status_code == 404


def test_delete_expense_not_found(auth_client):
    response = auth_client.delete("/api/expenses/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_delete_expense_does_not_affect_others(auth_client):
    r1 = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    r2 = auth_client.post("/api/expenses/", json={**VALID_PAYLOAD, "name": "Dinner"})
    auth_client.delete(f"/api/expenses/{r1.json()['id']}")
    list_resp = auth_client.get("/api/expenses/")
    body = list_resp.json()
    assert body["total"] == 1
    assert body["data"][0]["id"] == r2.json()["id"]


def test_delete_expense_twice(auth_client):
    create_resp = auth_client.post("/api/expenses/", json=VALID_PAYLOAD)
    expense_id = create_resp.json()["id"]
    assert auth_client.delete(f"/api/expenses/{expense_id}").status_code == 204
    assert auth_client.delete(f"/api/expenses/{expense_id}").status_code == 404
