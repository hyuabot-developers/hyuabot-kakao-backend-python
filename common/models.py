from pydantic import BaseModel
from typing import Optional


# class Intent(BaseModel):
#     id: Optional[str]
#     name: Optional[str]
#
#
# class Params(BaseModel):
#     ignoreMe: Optional[str]
#
#
# class Block(BaseModel):
#     id: Optional[str]
#     name: Optional[str]


class User(BaseModel):
    id: str
    # type: Optional[str]
    # properties: Optional[dict]


# class Bot(BaseModel):
#     id: Optional[str]
#     name: Optional[str]


# class Action(BaseModel):
#     name: Optional[str]
#     clientExtra: Optional[str]
#     params: Optional[dict]
#     id: Optional[str]
#     detailParams: Optional[dict]


class UserRequest(BaseModel):
    timezone: Optional[str]
    # params: Params
    # block: Block
    utterance: str
    # lang: Optional[str]
    user: User


class KakaoRequest(BaseModel):
    # intent: Intent
    userRequest: UserRequest
    # bot: Bot
    # action: Action


class ShuttleRequest(KakaoRequest):
    class Config:
        schema_extra = {
            'example': {
                "intent": {
                    "id": "BlockID",
                    "name": "BlockName"
                },
                "userRequest": {
                    "timezone": "Asia/Seoul",
                    "params": {
                        "ignoreMe": "true"
                    },
                    "block": {
                        "id": "BlockID",
                        "name": "BlockName"
                    },
                    "utterance": "🏫 셔틀콕",
                    "lang": None,
                    "user": {
                        "id": "469871",
                        "type": "accountId",
                        "properties": {}
                    }
                },
                "bot": {
                    "id": "BotID",
                    "name": "BotName"
                },
                "action": {
                    "name": "ActionName",
                    "clientExtra": None,
                    "params": {},
                    "id": "ActionID",
                    "detailParams": {}
                }
            }
        }


class FoodRequest(KakaoRequest):
    class Config:
        schema_extra = {
            'example': {
                "intent": {
                    "id": "BlockID",
                    "name": "BlockName"
                },
                "userRequest": {
                    "timezone": "Asia/Seoul",
                    "params": {
                        "ignoreMe": "true"
                    },
                    "block": {
                        "id": "BlockID",
                        "name": "BlockName"
                    },
                    "utterance": "교직원식당의 식단입니다",
                    "lang": None,
                    "user": {
                        "id": "469871",
                        "type": "accountId",
                        "properties": {}
                    }
                },
                "bot": {
                    "id": "BotID",
                    "name": "BotName"
                },
                "action": {
                    "name": "ActionName",
                    "clientExtra": None,
                    "params": {},
                    "id": "ActionID",
                    "detailParams": {}
                }
            }
        }


class ReadingRoomRequest(KakaoRequest):
    class Config:
        schema_extra = {
            'example': {
                "intent": {
                    "id": "BlockID",
                    "name": "BlockName"
                },
                "userRequest": {
                    "timezone": "Asia/Seoul",
                    "params": {
                        "ignoreMe": "true"
                    },
                    "block": {
                        "id": "BlockID",
                        "name": "BlockName"
                    },
                    "utterance": "제3열람실의 좌석정보입니다",
                    "lang": None,
                    "user": {
                        "id": "469871",
                        "type": "accountId",
                        "properties": {}
                    }
                },
                "bot": {
                    "id": "BotID",
                    "name": "BotName"
                },
                "action": {
                    "name": "ActionName",
                    "clientExtra": None,
                    "params": {},
                    "id": "ActionID",
                    "detailParams": {}
                }
            }
        }


class ShuttleStopRequest(KakaoRequest):
    class Config:
        schema_extra = {
            'example': {
                "intent": {
                    "id": "BlockID",
                    "name": "BlockName"
                },
                "userRequest": {
                    "timezone": "Asia/Seoul",
                    "params": {
                        "ignoreMe": "true"
                    },
                    "block": {
                        "id": "BlockID",
                        "name": "BlockName"
                    },
                    "utterance": "한대앞역 정류장 정보입니다.",
                    "lang": None,
                    "user": {
                        "id": "469871",
                        "type": "accountId",
                        "properties": {}
                    }
                },
                "bot": {
                    "id": "BotID",
                    "name": "BotName"
                },
                "action": {
                    "name": "ActionName",
                    "clientExtra": None,
                    "params": {},
                    "id": "ActionID",
                    "detailParams": {}
                }
            }
        }