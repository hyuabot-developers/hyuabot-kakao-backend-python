from pydantic import BaseModel, Field


class QuickReply(BaseModel):
    action: str = Field(alias="action")
    label: str = Field(alias="label")
    message_text: str = Field(alias="messageText")
    block_id: str = Field(alias="blockId")


class CardButton(BaseModel):
    action: str = Field(alias="action")
    label: str = Field(alias="label")
    web_link: str = Field(alias="webLinkLabel")


class TextCard(BaseModel):
    title: str = Field(alias="title")
    description: str = Field(alias="description")
    buttons: list[CardButton] = Field(alias="buttons")


class Carousel(BaseModel):
    type_string: str = Field(alias="type")
    items: list[TextCard] = Field(alias="items")


class TextContent(BaseModel):
    text: str = Field(alias="text")


class SimpleTextResponse(BaseModel):
    simple_text: TextContent = Field(alias="simpleText")


class BasicCardResponse(BaseModel):
    basic_card: TextCard = Field(alias="basicCard")


class CarouselResponse(BaseModel):
    carousel: Carousel = Field(alias="carousel")


class SkillTemplate(BaseModel):
    outputs: list[SimpleTextResponse | BasicCardResponse | CarouselResponse] = Field(alias="outputs")
    quick_replies: list[QuickReply] = Field(alias="quickReplies")


class ServerResponse(BaseModel):
    version: str = Field(alias="version")
    template: SkillTemplate = Field(alias="template")
