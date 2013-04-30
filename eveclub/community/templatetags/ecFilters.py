#coding: utf-8

import re
import markdown as m
from HTMLParser import HTMLParser
from django import template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def f_markdown(value):
    result = m.markdown(force_text(value), safe_mode=True, enable_attributes=False)
    result = result.replace('[HTML_REMOVED]', '')
    return result

def f_breakline(value):
    result = value.replace('\n', '<br />\n')
    result = result.replace('</p><br />', '</p>')
    result = result.replace('<blockquote><br />', '<blockquote>')
    result = result.replace('</blockquote><br />', '</blockquote>')
    return result

def f_emotion(value):
    import re
    pattern = re.compile(r'\[em (ac)(\d{2})\]')
    html = r'<img class="emotion_\1" src="/static/img/em/\1\2.gif" />'
    result = pattern.sub(html, value)
    return result

def f_striphtml(value):
    s = MLStripper()
    s.feed(value)
    return s.get_data()

def f_unescape(value):
    s = MLStripper()
    return s.unescape(value)

@register.filter(is_safe=True)
def markdown(value):
    result = f_markdown(value)
    result = f_breakline(result)
    result = f_emotion(result)
    return mark_safe(result)