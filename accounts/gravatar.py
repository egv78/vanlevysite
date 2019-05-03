# http://en.gravatar.com/site/implement/images/django/
import hashlib
import urllib
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()

# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url_identicon(email, size=160):
    default = "identicon"
    return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.encode('utf-8').lower()).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))


def gravatar_url_monsterid(email, size=160):
    default = "monsterid"
    return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.encode('utf-8').lower()).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))


def gravatar_url_wavatar(email, size=160):
    default = "wavatar"
    return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.encode('utf-8').lower()).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))


def gravatar_url_retro(email, size=160):
    default = "retro"
    return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.encode('utf-8').lower()).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))


def gravatar_url_robohash(email, size=160):
    default = "robohash"
    return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.encode('utf-8').lower()).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))
