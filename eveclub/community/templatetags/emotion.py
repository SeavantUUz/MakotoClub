#coding: utf-8

from django import template

register = template.Library()

# 支持AC站表情
@register.filter(is_safe=True)
def emotion(value):
    import re
    pattern = re.compile(r'\[em (ac)(\d{2})\]')
    html = r'<img class="emotion_\1" src="/static/img/em/\1\2.gif" />'
    result, number = pattern.subn(html, value)
    return result