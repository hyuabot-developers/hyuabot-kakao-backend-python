from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(alias="id")


class UserRequest(BaseModel):
    timezone: str | None = Field(alias="timezone")
    utterance: str = Field(alias="utterance")
    lang: str | None = Field(alias="lang")
    user: User = Field(alias="user")


class KakaoRequest(BaseModel):
    user_request: UserRequest = Field(alias="userRequest")
