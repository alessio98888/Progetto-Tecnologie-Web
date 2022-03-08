from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.urls import reverse

from user_profile.models import Language, Skill, Education, Certification, LanguageProficiency


class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    birth_date = models.DateField(default=None, null=True, blank=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    photo = models.ImageField(default=None, null=True, blank=True, upload_to="profile_photos")
    description = models.TextField(default="", blank=True, null=True)
    languages = models.ManyToManyField(LanguageProficiency, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    education = models.ManyToManyField(Education, blank=True)
    certifications = models.ManyToManyField(Certification, blank=True)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    @property
    def mean_rank(self):
        offers = self.offers.all()
        offers_count = offers.count()
        if offers_count == 0:
            return 0
        return sum([offer.rank for offer in offers])/offers_count

    @property
    def mean_stars(self):
        offers = self.offers.all()
        offers_count_with_reviews = sum(1 for offer in offers if offer.mean_stars_review is not None)
        if offers_count_with_reviews == 0:
            return 0
        return sum([offer.mean_stars_review for offer in offers if offer.mean_stars_review is not None]) / offers_count_with_reviews

    @property
    def total_review_count(self):
        offers = self.offers.all()
        offers_count = offers.count()
        if offers_count == 0:
            return 0
        return sum([offer.review_count for offer in offers])

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_management:home', args=[str(self.id)])

    class Meta:
        verbose_name = "User"
