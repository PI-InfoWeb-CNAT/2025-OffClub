from django import template
from django.conf import settings

register = template.Library()


@register.filter
def offer_image_url(image_field):
    """Return a URL for an ImageField that maps static defaults to STATIC_URL.

    - If image_field is falsy -> None
    - If image_field.name starts with 'static/' -> return STATIC_URL + path
    - Otherwise try image_field.url, fallback to MEDIA_URL + name
    """
    if not image_field:
        return None

    name = getattr(image_field, 'name', '') or ''
    idx = name.find('static/')
    if idx != -1:
        tail = name[idx + len('static/'):]
        return settings.STATIC_URL.rstrip('/') + '/' + tail.lstrip('/')

    try:
        return image_field.url
    except Exception:
        if name:
            return settings.MEDIA_URL.rstrip('/') + '/' + name.lstrip('/')
        return None
