import util

# DRESS_TYPES = ['gown', 'tulle', 'layer', 'stretch', 'pencil', 'ribbon', 'skirt',
#                'split', 'sheath', 'maxi', 'chiffon', 'bodice', 'wrap', 'lace',
#                'georgette', 'ruch', 'flare', 'simple', 'summer', 'ponte', 'peplum',
#                'satin', 'exposed']
# DRESS_ATTRIBUTES = ['hook', 'jewel', 'embroider', 'belt', 'strapless', 'polka',
#                     'floral', 'knit', 'waistband', 'knee', 'cutout', 'fit', 'slit',
#                     'sleeveless', 'a-line', 'spaghetti', 'v-neck', 'boat', 'sweetheart',
#                     'crew','surplice']

DRESS_TYPES = ['gown', 'tulle', 'layer', 'stretch', 'pencil', 'ribbon', 'skirt',
               'split', 'sheath', 'maxi', 'chiffon', 'bodice', 'wrap', 'lace',
               'georgette', 'flare', 'simple', 'summer', 'ponte', 'peplum',
               'satin', 'exposed', 'fit', 'slit']

DRESS_ATTRIBUTES = ['hook', 'jewel', 'embroider', 'belt', 'strapless', 'polka',
                    'floral', 'knit', 'waistband', 'knee', 'cutout',
                    'sleeveless', 'a-line', 'spaghetti', 'v-neck', 'boat', 'sweetheart',
                    'crew','surplice','ruch']

def parse(name, description):
    global DRESS_TYPES, DRESS_ATTRIBUTES
    types, attributes = set(), set()

    if 'mini' in name or 'Mini' in name or 'MINI' in name:
        types.add('mini')

    dsplit = description.strip().split()
    for token in dsplit:
        if not token:
            continue
        if is_syntax(token):
            continue
        normalized = token.lower()
        for dtype in DRESS_TYPES:
            if dtype in normalized:
                types.add(dtype)
        for dattr in DRESS_ATTRIBUTES:
            if dattr in normalized:
                attributes.add(dattr)

    return types, attributes

def is_syntax(token):
    return token[0] == '<' and token[-1] == '>'
