from django.contrib import admin

# Register your models here.
from user_profile.models import LanguageLevel, ExperienceLevel, Language

admin.site.register(LanguageLevel)
admin.site.register(ExperienceLevel)
admin.site.register(Language)
