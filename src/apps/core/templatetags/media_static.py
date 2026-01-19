from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


@register.filter(name='media_to_static')
def media_to_static(value):
    if not value:
        return ''

    # If it's a FileField or similar with .name
    try:
        name = getattr(value, 'name', None)
        if name:
            if name.startswith('static/'):
                return static(name[7:])
            # return URL if available
            return getattr(value, 'url', '')
    except Exception:
        pass

    s = str(value)
    media_url = settings.MEDIA_URL or '/uploads/'
    # If starts with MEDIA_URL and contains static/
    if s.startswith(media_url):
        rest = s[len(media_url):]
        if rest.startswith('static/'):
            return static(rest[len('static/'):])
        return s

    if s.startswith('/uploads/static/'):
        return static(s.split('/uploads/static/', 1)[1])

    if s.startswith('/static/'):
        return s

    if s.startswith('static/'):
        return static(s[len('static/'):])

    return s
