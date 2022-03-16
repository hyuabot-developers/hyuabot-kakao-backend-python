from pydantic import BaseModel


class User(BaseModel):
    id: str


class UserRequest(BaseModel):
    timezone: str | None
    utterance: str
    lang: str | None
    user: User


class KakaoRequest(BaseModel):
    userRequest: UserRequest
