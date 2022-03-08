from django.urls import path
from user_profile import views

app_name = "user_profile"

urlpatterns = [
    path("language/add/<int:pk>", views.language_proficiency_add, name="language-add"),
    path("language/delete/<int:pk>/<int:pk_language_proficiency>", views.language_proficiency_delete, name="language-delete"),
    path("language/update/<int:pk>/<int:pk_language_proficiency>", views.language_proficiency_update, name="language-update"),
    path("personal_info/update/<int:pk>", views.UserInfoUpdate.as_view(), name="personal_info-update"),
    path("personal_info/updatePhoto/<int:pk>", views.UserPhotoUpdate.as_view(), name="personal_info-updatePhoto"),
    path("skill/add/<int:pk>", views.skill_add, name="skill-add"),
    path("skill/delete/<int:pk>/<int:pk_skill>", views.skill_delete, name="skill-delete"),
    path("skill/update/<int:pk>/<int:pk_skill>", views.skill_update, name="skill-update"),
    path("education/add/<int:pk>", views.education_add, name="education-add"),
    path("education/delete/<int:pk>/<int:pk_education>", views.education_delete, name="education-delete"),
    path("education/update/<int:pk>/<int:pk_education>", views.education_update, name="education-update"),
    path("certification/add/<int:pk>", views.certification_add, name="certification-add"),
    path("certification/delete/<int:pk>/<int:pk_certification>", views.certification_delete, name="certification-delete"),
    path("certification/update/<int:pk>/<int:pk_certification>", views.certification_update, name="certification-update"),

]