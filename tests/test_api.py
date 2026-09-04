import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_and_booking_flow(client: AsyncClient):
    register_payload = {
        "email": "developer@example.com",
        "password": "strongpassword123",
        "full_name": "Test Engineer",
    }
    reg_resp = await client.post("/api/v1/auth/register", json=register_payload)
    assert reg_resp.status_code == 201
    assert reg_resp.json()["email"] == "developer@example.com"

    login_data = {
        "username": "developer@example.com",
        "password": "strongpassword123",
    }
    login_resp = await client.post("/api/v1/auth/login", data=login_data)
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    event_payload = {
        "title": "Python Backend Meetup",
        "description": "Highload architecture discussion",
        "location": "Online",
        "start_time": "2026-10-15T18:00:00Z",
        "total_seats": 2,
    }
    event_resp = await client.post("/api/v1/events/", json=event_payload, headers=headers)
    assert event_resp.status_code == 201
    event_id = event_resp.json()["id"]

    ticket_payload = {"event_id": event_id}
    ticket_resp = await client.post("/api/v1/tickets/", json=ticket_payload, headers=headers)
    assert ticket_resp.status_code == 201
    assert ticket_resp.json()["event_id"] == event_id

    duplicate_resp = await client.post("/api/v1/tickets/", json=ticket_payload, headers=headers)
    assert duplicate_resp.status_code == 400