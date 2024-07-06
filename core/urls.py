from django.urls import  path

from . import views

urlpatterns = [
    path('all/', views.problems_page, name="problems_page"),
    path('add/', views.add_problem, name="add_problem")
]