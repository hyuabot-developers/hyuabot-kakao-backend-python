from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field


class Button(BaseModel):
    label: Annotated[str, Field(alias='label')]
    action: Annotated[str, Field(alias='action')]
    web_link_url: Annotated[Optional[str], Field(alias='webLinkUrl', default=None)]
    message_text: Annotated[Optional[str], Field(alias='messageText', default=None)]
    phone_number: Annotated[Optional[str], Field(alias='phoneNumber', default=None)]
    block_id: Annotated[Optional[str], Field(alias='blockId', default=None)]
    extra: Annotated[Optional[dict[str, Any]], Field(alias='extra', default=None)]


class Link(BaseModel):
    pc: Annotated[Optional[str], Field(alias='pc', default=None)]
    mobile: Annotated[Optional[str], Field(alias='mobile', default=None)]
    web: Annotated[Optional[str], Field(alias='web', default=None)]


class Thumbnail(BaseModel):
    image_url: Annotated[str, Field(alias='imageUrl')]
    link: Annotated[Optional[Link], Field(alias='link', default=None)]
    fixed_ratio: Annotated[bool, Field(alias='fixedRatio', default=False)]


class CarouselHeader(BaseModel):
    title: Annotated[str, Field(alias='title')]
    thumbnail: Annotated[Thumbnail, Field(alias='thumbnail')]
    description: Annotated[str, Field(alias='description')]


class Component(BaseModel):
    pass


class SimpleTextItem(BaseModel):
    text: Annotated[str, Field(alias='text')]


class SimpleText(Component):
    simple_text: Annotated[SimpleTextItem, Field(alias='simpleText')]


class SimpleImageItem(BaseModel):
    image_url: Annotated[str, Field(alias='imageUrl')]
    alt_text: Annotated[str, Field(alias='altText')]


class SimpleImage(Component):
    simple_image: Annotated[SimpleImageItem, Field(alias='simpleImage')]


class TextCardItem(BaseModel):
    title: Annotated[str, Field(alias='title')]
    description: Annotated[str, Field(alias='description')]
    buttons: Annotated[Optional[list[Button]], Field(alias='buttons', default=None)]


class TextCard(Component):
    text_card: Annotated[TextCardItem, Field(alias='textCard')]


class BasicCardItem(BaseModel):
    title: Annotated[Optional[str], Field(alias='title', default=None)]
    description: Annotated[Optional[str], Field(alias='description', default=None)]
    thumbnail: Annotated[Optional[SimpleImage], Field(alias='thumbnail', default=None)]
    buttons: Annotated[Optional[list[Button]], Field(alias='buttons', default=None)]


class BasicCard(Component):
    basic_card: Annotated[BasicCardItem, Field(alias='basicCard')]


class CarouselItem(Component):
    type_: Annotated[str, Field(alias='type', default='basicCard')]
    items: Annotated[list[BasicCardItem | TextCardItem], Field(alias='items', min_items=1, max_items=10)]
    header: Annotated[Optional[CarouselHeader], Field(alias='header', default=None)]


class Carousel(Component):
    carousel: Annotated[CarouselItem, Field(alias='carousel')]


class QuickReply(BaseModel):
    label: Annotated[str, Field(alias='label')]
    action: Annotated[str, Field(alias='action')]
    message_text: Annotated[str, Field(alias='messageText')]
    block_id: Annotated[str, Field(alias='blockId')]
    extra: Annotated[dict[str, Any], Field(alias='extra')]


class Template(BaseModel):
    quick_replies: Annotated[list[QuickReply], Field(alias='quickReplies', default=None)]


class SimpleTextTemplate(Template):
    outputs: Annotated[list[SimpleText], Field(alias='outputs')]


class SimpleImageTemplate(Template):
    outputs: Annotated[list[SimpleImage], Field(alias='outputs')]


class BasicCardTemplate(Template):
    outputs: Annotated[list[BasicCard], Field(alias='outputs')]


class CarouselTemplate(Template):
    outputs: Annotated[list[Carousel], Field(alias='outputs')]


class ContextValue(BaseModel):
    name: Annotated[str, Field(alias='name')]
    life_span: Annotated[int, Field(alias='lifeSpan')]
    params: Annotated[dict[str, str], Field(alias='params')]


class ContextControl(BaseModel):
    values: Annotated[ContextValue, Field(alias='values')]


class Response(BaseModel):
    version: Annotated[str, Field(alias='version', default='2.0')]
    template: Annotated[Template, Field(alias='template')]
    context: Annotated[Optional[ContextControl], Field(alias='context', default=None)]
    data: Annotated[Optional[dict[str, Any]], Field(alias='data', default=None)]


class SimpleTextResponse(Response):
    template: Annotated[SimpleTextTemplate, Field(alias='template')]


class SimpleImageResponse(Response):
    template: Annotated[SimpleImageTemplate, Field(alias='template')]


class BasicCardResponse(Response):
    template: Annotated[BasicCardTemplate, Field(alias='template')]


class CarouselResponse(Response):
    template: Annotated[CarouselTemplate, Field(alias='template')]
