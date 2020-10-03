from copy import deepcopy

# 기본 답변
base_response = {'version': '2.0', 'template': {'outputs': [], 'quickReplies': []}}


# 카카오톡 채널 - 텍스트 응답
def insert_text(text):
    new_response = deepcopy(base_response)
    new_response['template']['outputs'] = [{"simpleText": {"text": text}}]
    return new_response


# 카카오톡 채널 - 이미지 응답
def insert_image(image_url, alt_text):
    new_response = deepcopy(base_response)
    new_response['template']['outputs'] = [{"simpleImage": {"imageUrl": image_url, "altText": alt_text}}]
    return new_response


# 카카오톡 채널 - 카드 응답
def insert_card(title, description, image_url=None, width=None, height=None):
    new_response = deepcopy(base_response)
    if image_url != None:
        if width != None and height != None:
            new_response['template']['outputs'] = [{'basicCard': {
                'title': title,
                'description': description,
                'thumbnail': {"imageUrl": image_url, 'fixedRatio': True, 'width': width, 'height': height},
                'buttons': []
            }}]
        else:
            new_response['template']['outputs'] = [{'basicCard': {
                'title': title,
                'description': description,
                'thumbnail': {"imageUrl": image_url},
                'buttons': []
            }}]
    else:
        new_response['template']['outputs'] = [{'basicCard': {
            'title': title,
            'description': description,
            'buttons': []
        }}]
    return new_response


# 카카오톡 채널 - 카드 버튼 추가
def insert_button(new_response, label, webUrl):
    new_response['template']['outputs'][0]['basicCard']['buttons'].append({
        "action": "webLink",
        "label": label,
        "webLinkUrl": webUrl
    })
    return new_response


# 카카오톡 채널 - 하단 버튼 추가
def insert_replies(new_response, reply):
    new_response['template']['quickReplies'].append(reply)
    return new_response


# 카카오톡 채널 - 하단 버튼 생성
def make_reply(label, message, block_id):
    return {'action': 'block', 'label': label, 'messageText': message, 'blockId': block_id}
