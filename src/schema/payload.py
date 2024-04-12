from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field


class Intent(BaseModel):
    id_: Annotated[str, Field(alias='id')]
    name: Annotated[str, Field(alias='name')]


class Block(BaseModel):
    id_: Annotated[str, Field(alias='id')]
    name: Annotated[str, Field(alias='name')]


class User(BaseModel):
    id_: Annotated[str, Field(alias='id')]
    type_: Annotated[str, Field(alias='type', default='botUserKey')]
    properties: Annotated[dict[str, Any], Field(alias='properties')]


class Bot(BaseModel):
    id_: Annotated[str, Field(alias='id')]
    name: Annotated[str, Field(alias='name')]


class DetailParams(BaseModel):
    origin: Annotated[str, Field(alias='origin')]
    value: Annotated[str, Field(alias='value')]
    group_name: Annotated[str, Field(alias='groupName')]


class Action(BaseModel):
    id_: Annotated[str, Field(alias='id')]
    name: Annotated[str, Field(alias='name')]
    params: Annotated[dict[str, str], Field(alias='params')]
    detail_params: Annotated[dict[str, DetailParams], Field(alias='detailParams')]
    client_extra: Annotated[Optional[dict[str, Any]], Field(alias='clientExtra', default=None)]


class UserRequest(BaseModel):
    timezone: Annotated[str, Field(alias='timezone')]
    block: Annotated[Block, Field(alias='block')]
    utterance: Annotated[str, Field(alias='utterance')]
    language: Annotated[Optional[str], Field(alias='lang', default=None)]
    user: Annotated[User, Field(alias='user')]


class Payload(BaseModel):
    intent: Annotated[Intent, Field(alias='intent')]
    user_request: Annotated[UserRequest, Field(alias='userRequest')]
    bot: Annotated[Bot, Field(alias='bot')]
    action: Annotated[Action, Field(alias='action')]

    class Config:
        json_schema_extra = {
            "example": {
                "intent": {
                    "id": "블록 ID",
                    "name": "블록 이름",
                },
                "userRequest": {
                    "timezone": "Asia/Seoul",
                    "params": {
                        "ignoreMe": "true",
                    },
                    "block": {
                        "id": "블록 ID",
                        "name": "블록 이름",
                    },
                    "utterance": "발화 내용",
                    "lang": "ko",
                    "user": {
                        "id": "077103",
                        "type": "accountId",
                        "properties": {},
                    },
                },
                "bot": {
                    "id": "봇 ID",
                    "name": "봇 이름",
                },
                "action": {
                    "name": "actionName",
                    "clientExtra": None,
                    "params": {},
                    "id": "actionId",
                    "detailParams": {},
                },
            },
        }
