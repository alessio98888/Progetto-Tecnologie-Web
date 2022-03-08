from django.contrib import admin

# Register your models here.
from posts.models import Currency, Category, Review, Offer

admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Offer)
#admin.site.register(Review)