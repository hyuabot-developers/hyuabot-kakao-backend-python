from app.hyuabot.kakao.scheme.response import TextCard, ServerResponse, SkillTemplate, \
    CarouselResponse, Carousel, QuickReply, CardButton, BasicCardResponse


def create_carousel_response(card_list: list[TextCard], quick_replies: list[QuickReply] = None) \
        -> ServerResponse:
    return ServerResponse(
        version="2.0",
        template=SkillTemplate(
            outputs=[
                CarouselResponse(
                    carousel=Carousel(type="basicCard", items=card_list),
                ),
            ],
            quickReplies=quick_replies,
        ),
    )


def create_basic_card_response(title: str, description: str,
                               buttons: list[CardButton], quick_replies: list[QuickReply] = None) \
        -> ServerResponse:
    return ServerResponse(
        version="2.0",
        template=SkillTemplate(
            outputs=[
                BasicCardResponse(basicCard=TextCard(
                    title=title, description=description, buttons=buttons,
                )),
            ],
            quickReplies=quick_replies,
        ),
    )
