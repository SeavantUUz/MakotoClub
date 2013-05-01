#coding: utf-8

import cgi
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

def f_raw_substr(value, length=10):
    """
    截取字符串，使得字符串长度等于length，并在字符串后加上省略号
    """
    is_encode = False
    try:
        str_encode = value.encode('gb18030') #为了中文和英文的长度一致（中文按长度2计算）
        is_encode = True
    except:
        pass
    if is_encode:
        l = length*2
        if l < len(str_encode):
            l = l - 3
            str_encode = str_encode[:l]
            try:
                value = str_encode.decode('gb18030') + '...'
            except:
                str_encode = str_encode[:-1]
                try:
                    value = str_encode.decode('gb18030') + '...'
                except:
                    is_encode = False
    if not is_encode:
        if length < len(value):
            length = length - 2
            return value[:length] + '...'
    return value

def f_substr(value, length=10):
    result = f_markdown(value)
    result = f_breakline(result)
    result = f_emotion(result)
    result = f_unescape(result)
    result = f_striphtml(result)
    result = f_raw_substr(result, length)
    result = cgi.escape(result)
    if result == '':
        result = u'......'
    return result


@register.filter(is_safe=True)
def raw_substr(value, length=10):
    return f_raw_substr(value, length)

@register.filter(is_safe=True)
def substr(value, length=10):
    return mark_safe(f_substr(value, length))