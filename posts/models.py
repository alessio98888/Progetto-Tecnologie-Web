from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg
from user_management.models import MyUser


class Currency(models.Model):
    symbol = models.CharField(max_length=1, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.symbol}"

    class Meta:
        verbose_name_plural = "Currencies"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField(default="", blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    currency = models.ForeignKey(Currency, default=1, on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Offer(Post):
    user = models.ForeignKey(MyUser, null=True, blank=True, default=None, on_delete=models.PROTECT,
                             related_name='offers')
    deleted_but_visible_home = models.BooleanField(default=False, blank=True)
    category = models.ForeignKey(Category, default=1, on_delete=models.PROTECT, related_name="offers")

    @property
    def mean_stars_review(self):
        return self.reviews.all().aggregate(Avg('stars'))['stars__avg']

    @property
    def review_count(self):
        review_list = self.reviews.order_by("-stars")
        return review_list.count()

    @property
    def rank(self):
        from scipy.stats import beta
        up = 1
        down = 1
        for i in range(1, 6):
            q = self.reviews.filter(stars=i).count()
            if q != 0:
                up += q * (i / 5)
                down += q * (1 - (i / 5))
        return beta.ppf(0.05, up, down)


class Review(models.Model):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5
    STARS_CHOICES = (
        (ONE_STAR, 'One'),
        (TWO_STARS, 'Two'),
        (THREE_STARS, 'Three'),
        (FOUR_STARS, 'Four'),
        (FIVE_STARS, 'Five'),
    )
    user = models.ForeignKey(MyUser, null=True, blank=True, default=None, on_delete=models.PROTECT,
                             related_name='reviews')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=STARS_CHOICES, default=THREE_STARS)
    comment = models.CharField(max_length=150, blank=True, null=True)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'offer',)


class OfferImage(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(default=None, null=True, blank=True, upload_to="offers_photos")


class Request(Post):
    user = models.ForeignKey(MyUser, null=True, blank=True, default=None, on_delete=models.PROTECT,
                             related_name='requests')
    category = models.ForeignKey(Category, default=1, on_delete=models.PROTECT, related_name="requests")
    pass


class OfferRequest(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="where_offered")
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="which_offered")

    class Meta:
        unique_together = ('offer', 'request',)


class BoughtOffers(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='bought_offers')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='users_who_bought')
    date = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = ('user', 'offer', )
