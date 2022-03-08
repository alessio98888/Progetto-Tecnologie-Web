from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
    path("offer/add/<int:pk>", views.OfferAdd.as_view(), name="offer-add"),
    path("offer/update/<int:pk>/<int:pk_offer>", views.offer_update, name="offer-update"),
    path("offer/delete/<int:pk>/<int:pk_offer>", views.offer_delete, name="offer-delete"),
    path("offer/update/visible/<int:pk>/<int:pk_offer>", views.offer_visible_update, name="offer-update-visible"),
    path("offer/update/photos/<int:pk>/<int:pk_offer>", views.OfferPhotosUpdate.as_view(), name="offer-update-photos"),
    path("offer/review/add/<int:pk>/<int:pk_offer>", views.offer_add_review, name="offer-add-review"),
    path("offer/review/<int:pk_offer>", views.offer_review_list, name="offer-review-list"),
    path("offer/detail/<int:pk>", views.OfferDetail.as_view(), name="offer-detail"),

    path("request/list/<int:pk>", views.request_list, name="request-list"),
    path("request/add/<int:pk>", views.RequestAdd.as_view(), name="request-add"),
    path("request/update/<int:pk>/<int:pk_request>", views.request_update, name="request-update"),
    path("request/delete/<int:pk>/<int:pk_request>", views.request_delete, name="request-delete"),
    path("request/detail/<int:pk>", views.RequestDetail.as_view(), name="request-detail"),
    path("request/add/offer/<int:pk_request>", views.offer_to_request, name="offer-to-request"),
    path("request/list/offers/<int:pk_request>", views.offers_for_request_list, name="offers-for-request-list"),

    path("offer/buy/<int:pk>/<int:pk_offer>", views.offer_buy, name="offer-buy"),
    path("offer/bought/list/<int:pk>", views.offers_bought_list, name="offers-bought-list"),

    path("offer/search", views.offer_search, name="offer-search"),

    path("seller/search", views.seller_search, name="seller-search"),

    path("orders/<int:pk>", views.orders, name="orders"),

]