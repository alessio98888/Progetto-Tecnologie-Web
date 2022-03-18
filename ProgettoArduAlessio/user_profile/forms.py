
from django import forms

from user_profile.models import LanguageProficiency, Skill, Education, Certification


class LanguageProficiencyForm(forms.ModelForm):

    class Meta:
        model = LanguageProficiency
        fields = ("name", "level",)


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ("description", "experience_level",)


class EducationForm(forms.ModelForm):

    class Meta:
        model = Education
        fields = ("country", "college", "title", "major", "graduation_year")


class CertificationForm(forms.ModelForm):

    class Meta:
        model = Certification
        fields = ("name", "certifiedFrom", "year",)


