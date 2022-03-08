import datetime

from django import template
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE
from django.urls import reverse


class Level(models.Model):
    level = models.CharField(max_length=50)
    levelInt = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.level}"

    class Meta:
        ordering = ['levelInt']
        abstract = True


class ExperienceLevel(Level):
    pass


class Skill(models.Model):
    description = models.CharField(max_length=30)
    experience_level = models.ForeignKey(ExperienceLevel, related_name='skills', on_delete=CASCADE)

    def __str__(self):
        return f"{self.description} - {self.experience_level}"

    def get_absolute_url(self):
        return reverse('skill_detail', args=[str(self.id)])

    def classname(self):
        return self.__class__.__name__


class LanguageLevel(Level):
    pass


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class LanguageProficiency(models.Model):
    name = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='languages')
    level = models.ForeignKey(LanguageLevel, on_delete=models.PROTECT, related_name='levels')

    def __str__(self):
        return f"{self.name} - {self.level}"

    def get_absolute_url(self):
        return reverse('language_detail', args=[str(self.id)])

    def classname(self):
        return self.__class__.__name__


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


year_dropdown = []
for y in range(1960, (current_year())):
    year_dropdown.append((y, y))


class Education(models.Model):
    country = models.CharField(max_length=50)
    college = models.CharField(max_length=75)
    major = models.CharField(max_length=75)
    title = models.CharField(max_length=75, default="")  # , null=True, blank=True, default="bo"
    graduation_year = models.IntegerField('Graduation Year', choices=year_dropdown,
                                          default=datetime.datetime.now().year,
                                          validators=[MinValueValidator(1960), max_value_current_year])

    def __str__(self):
        return f"{self.title} - {self.major} \n" \
               f"{self.college}, {self.country}, Graduated {self.graduation_year}"

    def classname(self):
        return self.__class__.__name__


class Certification(models.Model):
    name = models.CharField(max_length=75)
    certifiedFrom = models.CharField("Certified From", max_length=75)
    year = models.IntegerField('Year', choices=year_dropdown,
                               default=datetime.datetime.now().year,
                               validators=[MinValueValidator(1960), max_value_current_year])

    def __str__(self):
        return f"{self.name}. From {self.certifiedFrom}, {self.year}"

    def classname(self):
        return self.__class__.__name__
