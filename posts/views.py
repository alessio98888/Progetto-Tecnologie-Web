from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from django.views.generic.edit import FormView, UpdateView

from user_management.models import MyUser
from .forms import OfferAddForm, OfferUpdateForm, DeleteConfirmationForm, OfferAddReviewForm, \
    OfferPhotosUpdateForm, RequestAddForm, RequestUpdateForm, OfferSearchForm, SellerSearchForm
from .models import Offer, OfferImage, Review, Request, OfferRequest, BoughtOffers
from .templatetags.bought_count import bought_count


class OfferAdd(LoginRequiredMixin, FormView):
    form_class = OfferAddForm
    template_name = 'posts/offer/add.html'
    success_url = reverse_lazy("home")

    def get_success_url(self):
        pk = self.kwargs.get('pk', False)
        return reverse_lazy('user_management:home', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk', False)
        context['url'] = reverse_lazy("user_management:home", args=(pk,))

        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user_pk = kwargs.get('pk', False)
        user = MyUser.objects.get(pk=user_pk)
        files = request.FILES.getlist('image_field')
        if form.is_valid():
            offer = Offer(
                user=user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                currency=form.cleaned_data['currency'],
                category=form.cleaned_data['category'],
            )
            offer.save()
            for f in files:
                offer_image = OfferImage(offer=offer, photo=f)
                offer_image.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def offer_update(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_offer = kwargs.get("pk_offer", False)
    userObject = MyUser.objects.get(pk=pk)

    offer = userObject.offers.get(pk=pk_offer)

    if request.method == 'POST':
        form = OfferUpdateForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("user_management:home", args=(pk,)))
    else:
        return render(request, "posts/offer/update.html",
                      {"form": OfferUpdateForm(instance=offer),
                       "url": reverse_lazy("user_management:home", args=(pk,))})


@login_required
def offer_delete(request, **kwargs):
    pk = kwargs.get("pk", False)
    if request.method == 'POST':
        form = DeleteConfirmationForm(request.POST)
        if form.is_valid():
            pk_offer = kwargs.get("pk_offer", False)
            userObject = MyUser.objects.get(pk=pk)
            offer = userObject.offers.get(pk=pk_offer)
            if form.cleaned_data['deleted_but_visible_home'] is True:
                offer.deleted_but_visible_home = True
                offer.save()
            else:
                for image in offer.images.all():
                    image.photo.delete()
                    image.delete()
                userObject.offers.remove(offer)
                offer.delete()
            return redirect(reverse_lazy("user_management:home", args=(pk,)))
    else:
        return render(request, "posts/offer/delete.html",
                      {"form": DeleteConfirmationForm, "url": reverse_lazy("user_management:home", args=(pk,))})


@login_required
def offer_visible_update(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_offer = kwargs.get("pk_offer", False)
    userObject = MyUser.objects.get(pk=pk)
    offer = userObject.offers.get(pk=pk_offer)
    offer.deleted_but_visible_home = False
    offer.save()

    return redirect(reverse_lazy("user_management:home", args=(pk,)))


@login_required
def offer_add_review(request, pk="", pk_offer=""):
    user = MyUser.objects.get(pk=pk)  # user that wants to review
    offer = Offer.objects.get(pk=pk_offer)

    if request.method == 'POST':
        form = OfferAddReviewForm(request.POST)
        if form.is_valid():
            review = Review(
                user=user,
                offer=offer,
                stars=form.cleaned_data['stars'],
                comment=form.cleaned_data['comment'],
            )
            review.save()

            return redirect(reverse_lazy("user_management:home", args=(pk,), ))
    else:
        error_not_paid = False
        error_review_yourself = False

        if bought_count(user=user, offer=offer) == 0:
            error_not_paid = True

        # i can't review my own offers
        if offer.user == user:
            error_review_yourself = True

        context = {"error_review_yourself": error_review_yourself,
                   "error_not_paid": error_not_paid,
                   "form": OfferAddReviewForm,
                   "url": reverse_lazy("user_management:home", args=(pk,))
                   }

        return render(request, "posts/review/add.html", context)


class OfferList(ListView):
    model = Offer
    template_name = "posts/homepage_offer_list.html"

    ordering = ['date']


class OfferDetail(DetailView):
    model = Offer
    template_name = "posts/offer/detail.html"


class RequestDetail(DetailView):
    model = Request
    template_name = "posts/request/detail.html"


def offer_review_list(request, pk_offer):
    review_list = Offer.objects.get(pk=pk_offer).reviews.order_by("-stars")
    review_count = review_list.count()
    return render(request, "posts/review/offer_review_list.html", {"review_list": review_list, "review_count": review_count})


class OfferPhotosUpdate(LoginRequiredMixin, FormView):
    template_name = "posts/offer/update_photos.html"
    form_class = OfferPhotosUpdateForm

    def get_success_url(self):
        pk = self.kwargs.get('pk', False)
        return reverse_lazy('user_management:home', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', False)
        context['url'] = reverse_lazy("user_management:home", args=(pk,))
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user_pk = kwargs.get('pk', False)
        offer_pk = kwargs.get('pk_offer', False)
        user = MyUser.objects.get(pk=user_pk)
        offer = Offer.objects.get(pk=offer_pk)
        files = request.FILES.getlist('image_field')
        if form.is_valid():
            for image in offer.images.all():
                image.photo.delete()
                image.delete()

            for f in files:
                offer_image = OfferImage(offer=offer, photo=f)
                offer_image.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@login_required
def request_list(request, **kwargs):
    pk = kwargs.get("pk", False)
    userObject = MyUser.objects.get(pk=pk)
    requests = userObject.requests.all()

    context = {
        "userObject": userObject,
        "requests": requests,
    }
    return render(request, "posts/request/list.html", context)


class RequestAdd(LoginRequiredMixin, FormView):
    form_class = RequestAddForm
    template_name = 'posts/request/add.html'

    def get_success_url(self):
        pk = self.kwargs.get('pk', False)
        return reverse_lazy('posts:request-list', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', False)
        context['url'] = reverse_lazy("posts:request-list", args=(pk,))

        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user_pk = kwargs.get('pk', False)
        user = MyUser.objects.get(pk=user_pk)
        if form.is_valid():
            user_request = Request(
                user=user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                currency=form.cleaned_data['currency'],
                category=form.cleaned_data['category'],
            )
            user_request.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def request_update(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_request = kwargs.get("pk_request", False)
    userObject = MyUser.objects.get(pk=pk)

    user_request = userObject.requests.get(pk=pk_request)

    if request.method == 'POST':
        form = RequestUpdateForm(request.POST, instance=user_request)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("posts:request-list", args=(pk,)))
    else:
        return render(request, "posts/request/update.html",
                      {"form": RequestUpdateForm(instance=user_request),
                       "url": reverse_lazy("posts:request-list", args=(pk,))})


@login_required
def request_delete(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_request = kwargs.get("pk_request", False)
    userObject = MyUser.objects.get(pk=pk)
    user_request = userObject.requests.get(pk=pk_request)
    if request.method == 'POST':
        userObject.requests.remove(user_request)
        user_request.delete()
        return redirect(reverse_lazy("posts:request-list", args=(pk,)))
    else:
        return render(request, "posts/request/delete.html",
                      {"request": user_request, "url": reverse_lazy("posts:request-list", args=(pk,))})


@login_required
def offer_to_request(request, **kwargs):
    pk = request.user.pk
    userObject = MyUser.objects.get(pk=pk)
    pk_request = kwargs.get("pk_request", False)
    user_request = Request.objects.get(pk=pk_request)
    if request.method == 'POST':
        if "pk_offer" in request.POST:
            pk_offer = int(request.POST['pk_offer'])
            offer_request = OfferRequest(offer=Offer.objects.get(pk=pk_offer), request=user_request)
            offer_request.save()
        return redirect(reverse_lazy("home"))
    else:
        return render(request, "posts/request/add_offer.html",
                      {"request": user_request, "user_offers": userObject.offers.all()})


@login_required
def offers_for_request_list(request, **kwargs):
    # pk = request.user.pk
    # userObject = MyUser.objects.get(pk=pk)
    pk_request = kwargs.get("pk_request", False)

    user_request = Request.objects.get(pk=pk_request)
    if request.method == 'POST':
        return redirect(reverse_lazy("home"))
    else:
        return render(request, "posts/request/list_offers.html",
                      {"request": user_request, "pending_offers": user_request.which_offered.all()})


@login_required
def offer_buy(request, **kwargs):
    pk = kwargs.get("pk", False)
    userObject = MyUser.objects.get(pk=pk)
    pk_offer = kwargs.get("pk_offer", False)
    offer = Offer.objects.get(pk=pk_offer)

    if request.method == 'POST':
        bought_offer = BoughtOffers(offer=offer, user=userObject)
        bought_offer.save()
        return redirect(reverse_lazy("home"))
    else:
        return render(request, "posts/offer/buy.html", {"offer": offer, })


@login_required
def offers_bought_list(request, **kwargs):
    pk = kwargs.get("pk", False)
    userObject = MyUser.objects.get(pk=pk)

    # selecting distinct bought offers
    list_of_dict = userObject.bought_offers.values('offer').distinct()
    pk_offers = []
    for dic in list_of_dict:
        pk_offers.append(dic['offer'])

    return render(request, "posts/offer/bought_offers_list.html",
                      {"userObject": userObject, "bought_offers": Offer.objects.filter(pk__in=pk_offers)})


def offer_search(request, **kwargs):

    form = OfferSearchForm()

    if request.method == 'POST':
        form = OfferSearchForm(request.POST)
        if form.is_valid():
            price_bottom_threshold = form.cleaned_data['price_bottom_threshold']
            price_top_threshold = form.cleaned_data['price_top_threshold']
            category = form.cleaned_data['category']
            best_reviews = form.cleaned_data['best_reviews']

            offers = Offer.objects
            if price_bottom_threshold is not None:
                offers = offers.filter(price__gte=price_bottom_threshold)
            if price_top_threshold is not None:
                offers = offers.filter(price__lte=price_top_threshold)
            if category is not None:
                offers = offers.filter(category=category)

            if best_reviews:
                offers = sorted(offers.all(), key=lambda t: t.rank, reverse=True)
            else:
                offers = offers.all()

            return render(request, "posts/offer/search_results.html",
                      {"offers": offers})

    else:
        return render(request, "posts/offer/search.html",
                      {"form": form})


def seller_search(request, **kwargs):

    if request.POST:
        thresh = float(request.POST['thresh'])
        if thresh > 5 or thresh < 0:
            return render(request, "posts/seller_search.html", {"error": True})
        users = [user for user in MyUser.objects.all() if user.mean_stars >= thresh]
        sellers = sorted(users, key=lambda t: t.mean_rank, reverse=True)
        return render(request, "posts/seller_search_results.html",
                  {"sellers": sellers})
    else:
        return render(request, "posts/seller_search.html",)

# def seller_search(request, **kwargs):
#     sellers = sorted(MyUser.objects.all(), key=lambda t: t.mean_rank, reverse=True)
#     return render(request, "posts/seller_search_results.html",
#               {"sellers": sellers})


@login_required
def orders(request, **kwargs):
    pk = kwargs.get("pk", False)
    userObject = MyUser.objects.get(pk=pk)
    my_offers = userObject.offers.values()
    # selecting distinct bought offers

    pk_offers = []
    for dic in my_offers:
        pk_offers.append(dic['id'])

    return render(request, "posts/order/orders.html",
                  {"userObject": userObject, "orders": BoughtOffers.objects.filter(offer__in=pk_offers).order_by("date")})