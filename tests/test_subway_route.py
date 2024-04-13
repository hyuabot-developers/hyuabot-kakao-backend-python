import pytest
from async_asgi_testclient import TestClient


@pytest.mark.asyncio
async def test_subway_arrival(client: TestClient) -> None:
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

    response = await client.post("/subway", json=example_payload)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["version"] == "2.0"
    assert isinstance(response_json["template"], dict)
    assert isinstance(response_json["template"]["outputs"], list)
    assert isinstance(response_json["template"]["quickReplies"], list)
    for output in response_json["template"]["outputs"]:
        assert output.get("carousel") is not None
        carousel = output["carousel"]
        assert isinstance(carousel, dict)
        assert isinstance(carousel["items"], list)
        assert isinstance(carousel["type"], str)
        for item in carousel["items"]:
            assert item.get("title") is not None
            assert item.get("description") is not None
    for quick_reply in response_json["template"]["quickReplies"]:
        assert quick_reply.get("label") is not None
        assert quick_reply.get("action") is not None
        assert quick_reply.get("messageText") is not None
        assert quick_reply.get("blockId") is not None
        assert quick_reply.get("extra") is not None
