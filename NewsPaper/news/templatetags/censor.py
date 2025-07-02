from django import template
import re


register = template.Library()

@register.filter()
def censor(value):
    BAD_WORDS = ['бзд', 'говн', 'жоп', 'шлюх']

    if not isinstance(value, str):
        raise ValueError("Фильтр 'censor' применим только к строкам")

    def replace_match(match):
        word = match.group(0)
        return word[0] + '*' * (len(word) - 1)

    pattern = re.compile(r'\b\w*(' + '|'.join(map(re.escape, BAD_WORDS)) + r')\w*\b',
        flags=re.IGNORECASE)

    return pattern.sub(replace_match, value)