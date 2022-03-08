from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from user_management.forms import MyUserCreationForm
from user_management.models import MyUser


def user_detail(request, **kwargs):
    pk = kwargs.get("pk", False)
    userObject = MyUser.objects.get(pk=pk)
    languages = userObject.languages.all()
    skills = userObject.skills.all()
    education = userObject.education.all()
    certifications = userObject.certifications.all()
    offers = userObject.offers.order_by("-date")

    context = {
        "userObject": userObject,
        "languages": languages,
        "skills": skills,
        "education": education,
        "certifications": certifications,
        "offers": offers,
    }
    return render(request, "user_management/home.html", context)


class UserCreateView(CreateView):
    form_class = MyUserCreationForm
    template_name = "registration/user_create.html"
    success_url = reverse_lazy("home")


def check_username_is_unique(request):
    user = None
    username = request.GET.get('username', False)
    if username:
        user = MyUser.objects.filter(username=username)
    return JsonResponse({'is_not_unique': True if user else False})


def check_email_is_unique(request):
    user = None
    email = request.GET.get('email', False)
    if email:
        user = MyUser.objects.filter(email=email)
    return JsonResponse({'is_not_unique': True if user else False})