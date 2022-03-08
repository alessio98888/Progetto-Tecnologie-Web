from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from user_management.models import MyUser

from user_profile.forms import LanguageProficiencyForm, SkillForm, EducationForm, CertificationForm


@login_required
def language_proficiency_add(request, pk=""):
    userObject = MyUser.objects.get(pk=pk)
    if request.method == 'POST':

        form = LanguageProficiencyForm(request.POST)
        if form.is_valid():
            i = form.save()
            userObject.languages.add(i)
            return redirect(reverse_lazy("user_management:home", args=(pk,)))
    else:
        return render(request, "user_profile/language/add.html",
                      {"form": LanguageProficiencyForm, "url": reverse_lazy("user_management:home", args=(pk,))})


@login_required
def language_proficiency_delete(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_language_proficiency = kwargs.get("pk_language_proficiency", False)
    userObject = MyUser.objects.get(pk=pk)

    language_proficiency = userObject.languages.get(pk=pk_language_proficiency)
    userObject.languages.remove(language_proficiency)
    language_proficiency.delete()
    return redirect(reverse_lazy("user_management:home", args=(pk,)))


@login_required
def language_proficiency_update(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_language_proficiency = kwargs.get("pk_language_proficiency", False)
    userObject = MyUser.objects.get(pk=pk)

    language_proficiency = userObject.languages.get(pk=pk_language_proficiency)

    if request.method == 'POST':
        form = LanguageProficiencyForm(request.POST, instance=language_proficiency)
        if form.is_valid():
            form.save()

            return redirect(reverse_lazy("user_management:home", args=(pk,)))
    else:
        return render(request, "user_profile/language/update.html",
                      {"form": LanguageProficiencyForm(instance=language_proficiency), "url": reverse_lazy("user_management:home", args=(pk,))})


class UserInfoUpdate(LoginRequiredMixin, UpdateView):
    template_name = "user_profile/personal_info/change.html"
    model = MyUser
    fields = ("description", "first_name", "last_name", "birth_date",)

    def get_success_url(self):
        return reverse_lazy('user_management:home', kwargs={'pk': self.object.pk})


class UserPhotoUpdate(LoginRequiredMixin, UpdateView):
    template_name = "user_profile/personal_info/changePhoto.html"
    model = MyUser
    fields = ("photo",)

    def post(self, request, *args, **kwargs):
        user_pk = kwargs.get('pk', False)
        user = MyUser.objects.get(pk=user_pk)
        if 'cancel' in request.POST:
            return redirect(reverse_lazy('user_management:home', kwargs={'pk': user_pk}))
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            user.photo.delete()
            user.photo = form.cleaned_data['photo']
            user.save(update_fields=['photo'])
            return redirect(reverse_lazy('user_management:home', kwargs={'pk': user_pk}))
        else:
            return self.form_invalid(form)


@login_required
def skill_add(request, pk=""):
    userObject = MyUser.objects.get(pk=pk)

    if request.method == 'POST':

        form = SkillForm(request.POST)
        if form.is_valid():
            i = form.save()
            userObject.skills.add(i)

            return redirect(reverse_lazy("user_management:home", args=(pk,), ))
    else:
        return render(request, "user_profile/skill/add.html",
                      {"form": SkillForm, "url": reverse_lazy("user_management:home", args=(pk,))})


@login_required
def skill_delete(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_skill = kwargs.get("pk_skill", False)
    userObject = MyUser.objects.get(pk=pk)
    request.session["fromSkill"] = True
    skill = userObject.skills.get(pk=pk_skill)
    userObject.skills.remove(skill)
    skill.delete()
    #messages.add_message(request, messages.INFO, "fromSkill")
    return redirect(reverse_lazy("user_management:home", args=(pk,)))


@login_required
def skill_update(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_skill = kwargs.get("pk_skill", False)
    userObject = MyUser.objects.get(pk=pk)

    skill = userObject.skills.get(pk=pk_skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("user_management:home", args=(pk,)))
    else:
        return render(request, "user_profile/skill/update.html",
                      {"form": SkillForm(instance=skill), "url": reverse_lazy("user_management:home", args=(pk,))})


@login_required
def education_add(request, pk=""):
    userObject = MyUser.objects.get(pk=pk)

    if request.method == 'POST':

        form = EducationForm(request.POST)
        if form.is_valid():
            i = form.save()
            userObject.education.add(i)
            return redirect(reverse_lazy("user_management:home", args=(pk,)))

    else:
        return render(request, "user_profile/education/add.html",
                      {"form": EducationForm, "url": reverse_lazy("user_management:home", args=(pk,))})


@login_required
def education_delete(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_education = kwargs.get("pk_education", False)
    userObject = MyUser.objects.get(pk=pk)

    education = userObject.education.get(pk=pk_education)
    userObject.education.remove(education)
    education.delete()
    return redirect(reverse_lazy("user_management:home", args=(pk,)))


@login_required
def education_update(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_education = kwargs.get("pk_education", False)
    userObject = MyUser.objects.get(pk=pk)

    education = userObject.education.get(pk=pk_education)

    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("user_management:home", args=(pk,)))
    else:
        return render(request, "user_profile/education/update.html",
                      {"form": EducationForm(instance=education), "url": reverse_lazy("user_management:home", args=(pk,))})


@login_required
def certification_add(request, pk=""):
    userObject = MyUser.objects.get(pk=pk)

    if request.method == 'POST':

        form = CertificationForm(request.POST)
        if form.is_valid():
            i = form.save()
            userObject.certifications.add(i)
            return redirect(reverse_lazy("user_management:home", args=(pk,)))

    else:
        return render(request, "user_profile/certification/add.html",
                      {"form": CertificationForm, "url": reverse_lazy("user_management:home", args=(pk,))})


@login_required
def certification_delete(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_certification = kwargs.get("pk_certification", False)
    userObject = MyUser.objects.get(pk=pk)

    certification = userObject.certifications.get(pk=pk_certification)
    userObject.certifications.remove(certification)
    certification.delete()
    return redirect(reverse_lazy("user_management:home", args=(pk,)))


@login_required
def certification_update(request, **kwargs):
    pk = kwargs.get("pk", False)
    pk_certification = kwargs.get("pk_certification", False)
    userObject = MyUser.objects.get(pk=pk)

    certification = userObject.certifications.get(pk=pk_certification)

    if request.method == 'POST':
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("user_management:home", args=(pk,)))
    else:
        return render(request, "user_profile/certification/update.html",
                      {"form": CertificationForm(instance=certification), "url": reverse_lazy("user_management:home", args=(pk,))})