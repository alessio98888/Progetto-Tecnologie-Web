from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from posts.models import Offer, Category, Currency, Review
from user_management.models import MyUser
from scipy.stats import beta

from user_profile.models import Skill, ExperienceLevel, Language, LanguageLevel, LanguageProficiency, Education, \
    Certification


class Tests_add_professional_info(TestCase):
    def setUp(self):
        self.user = MyUser()
        self.user.email = "email1@gmail.com"
        self.user.username = "username1"
        self.user.save()
        self.client.force_login(self.user)

    def test_add_skill(self):
        self.level = ExperienceLevel(level="level", levelInt="1")
        self.level.save()
        response = self.client.post(
            reverse('user_profile:skill-add', kwargs={"pk": self.user.pk}),
            data={"description": "description", "experience_level": self.level.pk})
        self.assertIsNotNone(self.user.skills.get(pk=1))
        self.assertEqual(response.status_code, 302)

    def test_add_language_proficency(self):
        self.language = Language(name="language")
        self.language.save()
        self.languageLevel = LanguageLevel(level="languageLevel", levelInt=2)
        self.languageLevel.save()
        response = self.client.post(
            reverse('user_profile:language-add', kwargs={"pk": self.user.pk}),
            data={"name": self.language.pk, "level": self.languageLevel.pk})
        self.assertIsNotNone(self.user.languages.get(pk=1))
        self.assertEqual(response.status_code, 302)

    def test_add_education(self):
        response = self.client.post(
            reverse('user_profile:education-add', kwargs={"pk": self.user.pk}),
            data={"country":"country", "college":"college", "major":"major", "title":"title", "graduation_year":2000})
        self.assertIsNotNone(self.user.education.get(pk=1))
        self.assertEqual(response.status_code, 302)

    def test_add_certification(self):
        response = self.client.post(
            reverse('user_profile:certification-add', kwargs={"pk": self.user.pk}),
            data={"name":"name", "certifiedFrom":"from", "year":2000})
        self.assertIsNotNone(self.user.certifications.get(pk=1))
        self.assertEqual(response.status_code, 302)