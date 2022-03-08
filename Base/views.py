from django.shortcuts import render

# Create your views here.
from posts.models import Offer, Request, BoughtOffers, Review, Category
from django_pandas.io import read_frame
from scipy.stats import beta
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    recommended_offers = None
    if request.user.is_authenticated:
        bought_offers_queryset = BoughtOffers.objects.filter(user=request.user.pk).distinct().values_list('offer',
                                                                                                          flat=True)
        bought_offers = Offer.objects.filter(pk__in=list(bought_offers_queryset))
        list_bought = [offer for offer in bought_offers]
        categories_bought = list(set([offer.category for offer in list_bought]))
        categories_rank_for_user = {}
        review_count_perstar_percategory = {}

        for cat in categories_bought:
            for offer in list_bought:
                if offer.category.pk == cat.pk:
                    try:
                        review = Review.objects.get(user=request.user.pk, offer=offer.pk)
                    except ObjectDoesNotExist:
                        review = None

                    if review is not None:
                        if cat.pk not in review_count_perstar_percategory:
                            review_count_perstar_percategory[cat.pk] = dict()
                        if review.stars not in review_count_perstar_percategory[cat.pk]:
                            review_count_perstar_percategory[cat.pk][review.stars] = 0

                        review_count_perstar_percategory[cat.pk][review.stars] += 1

        for k, v in review_count_perstar_percategory.items():
            q = 0
            up = 1
            down = 1
            for i in range(1, 6):
                if i not in v:
                    q = 0
                else:
                    q = v[i]
                if q != 0:
                    up += q * (i / 5)
                    down += q * (1 - (i / 5))
            categories_rank_for_user[k] = beta.ppf(0.05, up, down)

        favorite_categories = sorted(list(categories_rank_for_user.items()), key=lambda t: t[1])[:2]

        recommended_offers = []
        for t in favorite_categories:
            cat_pk = t[0]
            recommended_offers.extend(sorted(
                Category.objects.get(pk=cat_pk).offers.exclude(user=request.user.pk).exclude(
                    pk__in=bought_offers_queryset), key=lambda t: t.rank, reverse=True))
    if recommended_offers:
        recommended_offers = [offer for offer in recommended_offers if offer.deleted_but_visible_home == False]
    context = {
        "offers_recently_added": Offer.objects.all().filter(deleted_but_visible_home=False).order_by("-date")[:10],
        "requests_recently_added": Request.objects.order_by("-date")[:10],
        "recommended_offers": recommended_offers,
    }

    return render(request, "home.html", context)
