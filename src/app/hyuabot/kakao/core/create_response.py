from app.hyuabot.kakao.scheme.response import TextCard, ServerResponse, SkillTemplate,\
    CarouselResponse, Carousel


def create_carousel_response(card_list: list[TextCard]) -> ServerResponse:
    return ServerResponse(
        version="2.0",
        template=SkillTemplate(
            outputs=[
                CarouselResponse(
                    carousel=Carousel(type="basicCard", items=card_list),
                )
            ],
            quickReplies=[],
        )
    )
