import pytest
from async_asgi_testclient import TestClient


@pytest.mark.asyncio
async def test_register_user(client: TestClient) -> None:
    example_payload = {
        "intent": {
            "id": "Intent ID",
            "name": "Intent Name",
        },
        "userRequest": {
            "timezone": "Asia/Seoul",
            "params": {
                "ignoreMe": "true",
            },
            "block": {
                "id": "Block ID",
                "name": "Block Name",
            },
            "utterance": "발화 내용",
            "lang": None,
            "user": {
                "id": "125621",
                "type": "accountId",
                "properties": {},
            },
        },
        "bot": {
            "id": "5cbf03fd5f38dd4c34bac577",
            "name": "봇 이름",
        },
        "action": {
            "name": "Action Name",
            "clientExtra": None,
            "params": {},
            "id": "Action ID",
            "detailParams": {},
        },
    }

    response = await client.post("/healthcheck", json=example_payload)
    assert response.status_code == 200
