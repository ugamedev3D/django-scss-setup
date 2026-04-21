from django import template
from django.urls import reverse


register = template.Library()

@register.simple_tag(takes_context=True)
def account_url(context, name):
    request = context["request"]
    request_name = (
        request.resolver_match.app_name or
        request.resolver_match.namespace
    )

    if request_name:
        url_name = f"{request_name}:{name}"
    else:
        url_name = name

    return reverse(url_name)

    