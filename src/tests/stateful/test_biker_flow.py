import requests

def test_biker_crud_flow(auth_headers):
    base_url = "http://127.0.0.1:8000/api/bikers/"

    # CREATE
    create_resp = requests.post(
        base_url,
        json={"name": "Test Biker"},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    biker_id = create_resp.json()["data"]["id"]

    # READ
    read_resp = requests.get(
        f"{base_url}detail/{biker_id}/",
        headers=auth_headers,
    )
    assert read_resp.status_code == 200

    # UPDATE
    update_resp = requests.patch(
        f"{base_url}detail/{biker_id}/",
        json={"name": "Updated Biker"},
        headers=auth_headers,
    )
    assert update_resp.status_code == 200

    # DELETE
    delete_resp = requests.delete(
        f"{base_url}detail/{biker_id}/",
        headers=auth_headers,
    )
    assert delete_resp.status_code in [200, 204]
