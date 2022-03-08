from django import template

from posts.models import BoughtOffers, Review

register = template.Library()


@register.simple_tag
def has_reviewed(offer, user):
    return True if Review.objects.filter(user=user, offer=offer).count() > 0 else False
