from decimal import Decimal

from django import forms
from django.forms import NumberInput

from posts.models import Offer, Review, Post, Request, Category


class OfferAddForm(forms.ModelForm):
    image_field = forms.ImageField(label="Images", widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Offer
        fields = ("title", "description", "category", "price", "currency",)


class OfferPhotosUpdateForm(forms.Form):
    image_field = forms.ImageField(label="Images", widget=forms.ClearableFileInput(attrs={'multiple': True}))


class OfferUpdateForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ("title", "description", "category", "price", "currency",)


class RequestUpdateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ("title", "description", "category", "price", "currency",)


class DeleteConfirmationForm(forms.Form):
    deleted_but_visible_home = forms.BooleanField(
        label="Check this if you want the offer to be not public but visible in your homepage",
        required=False
    )


class OfferAddReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ("stars", "comment", )


class RequestAddForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ("title", "description", "category", "price", "currency",)


class OfferSearchForm(forms.Form):
    category = forms.ModelChoiceField(Category.objects, required=False)
    best_reviews = forms.BooleanField(
        label="Order by best reviews",
        required=False)

    price_bottom_threshold = forms.DecimalField(decimal_places=2, max_digits=12, min_value=Decimal('0.01'), required=False, )
    price_top_threshold = forms.DecimalField(decimal_places=2, max_digits=12, min_value=Decimal('0.01'), required=False, )


class SellerSearchForm(forms.Form):
    count = forms.IntegerField(widget=NumberInput(attrs={'type': 'range', 'step': '2'}))
    pass
