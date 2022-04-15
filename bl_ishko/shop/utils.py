from django.utils.text import slugify
from time import time


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya', 'ь': ''}


def gen_slug(title, model_type=None):
    if model_type:
        eng_title = ''.join(alphabet.get(c, c) for c in title.lower())
        slug_field = ' '.join(eng_title.split()[:4]) + '-' + str(time())[-3:]
    else:
        slug_field = ''.join(alphabet.get(c, c) for c in title.lower())
    return slugify(slug_field, allow_unicode=True)