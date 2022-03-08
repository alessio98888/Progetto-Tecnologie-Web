from django import template

from posts.models import BoughtOffers

register = template.Library()


@register.simple_tag
def bought_count(offer, user):
    return BoughtOffers.objects.filter(user=user, offer=offer).count()
