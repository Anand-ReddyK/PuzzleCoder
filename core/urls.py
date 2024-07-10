from django.urls import  path

from . import views

urlpatterns = [
    path('problems/', views.problems_page, name="problems_page"),
    path('add/', views.add_problem, name="add_problem"),
    path("problem/<int:id>/", views.problem_detail, name="problem_detail")
]