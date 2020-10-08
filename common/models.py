from sanic import Blueprint
# Declare namespace object
kakao_url = Blueprint("kakao", url_prefix="/kakao")

# kakao_data = kakao_url.model(
#     'Default', {
#         'intent': fields.Nested(
#             model={
#                 'id': fields.String(example='7exhlpxxfhkkgwm8zo3emniq'),
#                 'name': fields.String(example='블록명')
#             },
#             description='Kakao i 내부의 intent의 block id'
#         ),
#         'userRequest': fields.Nested(
#             model={
#                 'timezone': fields.String(example='Asia/Seoul'),
#                 'params': fields.Nested(
#                     model={
#                         'ignoreMe': fields.String(example='true')
#                     }
#                 ),
#                 'block': fields.Nested(
#                     model={
#                         'id': fields.String(example='7exhlpxxfhkkgwm8zo3emniq', description='블록 ID'),
#                         'name': fields.String(example='블록 이름', description='블록 이름')
#                     }
#                 ),
#                 'utterance': fields.String(example='', description='발화 내용', required=True),
#                 'lang': fields.String(example=None, description='언어 설정'),
#                 'user': fields.Nested(
#                     model={
#                         'id': fields.String(example='276533', description='사용자별 고유번호', required=True),
#                         'type': fields.String(example='accountId', description='고유번호 종류'),
#                         'properties': fields.Nested(model={})
#                     }
#                 )
#             }
#         ),
#         'bot': fields.Nested(
#             model={
#                 'id': fields.String(example='5cbf03fd5f38dd4c34bac577', description='봇 일련번호'),
#                 'name': fields.String(example='봇 이름', description='봇 이름'),
#             }
#         ),
#         'action': fields.Nested(
#             model={
#                 'name': fields.String(example='tfwbmwzclo', description='액션 이름'),
#                 'clientExtra': fields.String(example=None),
#                 'params': fields.Nested(model={}),
#                 'id': fields.String(example='cn1hd5mm6ggpjai3utlm4gwp', description='액션 ID'),
#                 'detailParams': fields.Nested(model={}),
#             }
#         )
#     }
# )
