from django.test import TestCase
from django.urls import reverse

from posts.models import Offer, Category, Currency
from user_management.models import MyUser

from user_profile.models import Skill, ExperienceLevel, Language, LanguageLevel, LanguageProficiency, Education, \
    Certification


class Tests_userhome_without_professional_info(TestCase):

    def setUp(self):
        self.user = MyUser()
        self.user.email = "email1@gmail.com"
        self.user.username = "username1"
        self.user.save()

        self.category = Category()
        self.category.name = "Category test"
        self.category.description = "test"
        self.category.save()

        self.currency = Currency()
        self.currency.name = "currency test"
        self.currency.symbol = "t"
        self.currency.save()

        self.offer = Offer()
        self.offer.user = self.user
        self.offer.category = self.category
        self.offer.currency = self.currency
        self.offer.description = "Description"
        self.offer.price = 12
        self.offer.title = "Title"
        self.offer.save()

    def test_userhome_noinfo(self):
        response = self.client.get(reverse('user_management:home', kwargs={'pk': 1}))
        self.assertEqual(response.context['offers'][0].pk, 1)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['languages'], [])
        self.assertQuerysetEqual(response.context['skills'], [])
        self.assertQuerysetEqual(response.context['education'], [])
        self.assertQuerysetEqual(response.context['certifications'], [])


class Tests_userhome_with_info(TestCase):

    def setUp(self):
        self.user = MyUser()
        self.user.email = "email1@gmail.com"
        self.user.username = "username1"
        self.user.save()

        self.category = Category()
        self.category.name = "Category test"
        self.category.description = "test"
        self.category.save()

        self.currency = Currency()
        self.currency.name = "currency test"
        self.currency.symbol = "t"
        self.currency.save()

        self.offer = Offer()
        self.offer.user = self.user
        self.offer.category = self.category
        self.offer.currency = self.currency
        self.offer.description = "Description"
        self.offer.price = 12
        self.offer.title = "Title"
        self.offer.save()

        self.level = ExperienceLevel(level="level", levelInt="1")
        self.level.save()
        self.skill = Skill(description="description", experience_level=self.level)
        self.skill.save()


        self.language = Language(name="language")
        self.language.save()
        self.languageLevel = LanguageLevel(level="languageLevel", levelInt=2)
        self.languageLevel.save()
        self.languageProficiency = LanguageProficiency(name=self.language, level=self.languageLevel)
        self.languageProficiency.save()
        self.education = Education(country="country", college="college", major="major", title="title", graduation_year=2000)
        self.education.save()
        self.certification = Certification(name="name", certifiedFrom="from", year=2000)
        self.certification.save()

        self.user.skills.add(self.skill)
        self.user.languages.add(self.languageProficiency)
        self.user.education.add(self.education)
        self.user.certifications.add(self.certification)

    def test_userhome_with_info(self):
        response = self.client.get(reverse('user_management:home', kwargs={'pk': 1}))
        self.assertEqual(response.context['offers'][0].pk, 1)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['languages'], [repr(self.languageProficiency)])
        self.assertQuerysetEqual(response.context['skills'], [repr(self.skill)])
        self.assertQuerysetEqual(response.context['education'], [repr(self.education)])
        self.assertQuerysetEqual(response.context['certifications'], [repr(self.certification)])
