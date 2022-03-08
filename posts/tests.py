from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from posts.models import Offer, Category, Currency, Review
from user_management.models import MyUser
from scipy.stats import beta


class Tests(TestCase):
    def newTestOffer(self):
        o = Offer()
        o.user = self.user
        o.category = self.category
        o.currency = self.currency
        o.description = "Description"
        o.price = 12
        o.title = "Title"
        o.save()
        return o

    def setUp(self):
        self.user = MyUser()
        self.user.email = "email1@gmail.com"
        self.user.username = "username1"
        self.user.save()

        self.user2 = MyUser()
        self.user2.email = "email2@gmail.com"
        self.user2.username = "username2"
        self.user2.save()

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

        self.review = Review()
        self.review.user = self.user
        self.review.stars = self.review.FIVE_STARS
        self.review.comment = "comment test"
        self.review.offer = self.offer
        self.review.save()

        self.review = Review()
        self.review.user = self.user2
        self.review.stars = self.review.FOUR_STARS
        self.review.comment = "comment test"
        self.review.offer = self.offer
        self.review.save()

    def test_mean_stars_review(self):
        self.assertEqual(self.offer.mean_stars_review, (5 + 4) / 2)

    def test_review_count(self):
        self.assertEqual(self.offer.review_count, 2)

    def test_rank(self):
        self.assertEqual(self.offer.rank, beta.ppf(0.05, 14 / 5, 6 / 5))

    def test_rank_zero_reviews(self):
        self.assertEqual(self.newTestOffer().rank, 0.05)

    def test_mean_stars_review_zero_reviews(self):
        self.assertEqual(self.newTestOffer().mean_stars_review, None)



