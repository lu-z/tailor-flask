import re, util

DRESS_TYPES = []
DRESS_ATTRIBUTES = []

def parse(name, description):
    global DRESS_TYPES, DRESS_ATTRIBUTES
    types, attributes = [], []

    if 'mini' in name or 'Mini' in name or 'MINI' in name:
        types.append('mini')


    description = description.strip()
    dsplit = re.split(' |-', description)

    for token in dsplit:
        if not token:
            continue
        if is_syntax(token):
            continue
        normalized = token.lower()
        for dtype in DRESS_TYPES:
            if dtype in normalized:
                types.append(dtype)
        for dattr in DRESS_ATTRIBUTES:
            if dattr in normalized:
                attributes.append(dattr)

    return types, attributes

def is_syntax(token):
    return token[0] == '<' and token[-1] == '>'
