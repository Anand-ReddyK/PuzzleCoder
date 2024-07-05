from django.urls import  path

from . import views

urlpatterns = [
    path('all/', views.all_problems, name="all_problems"),
    path('add/', views.add_problem, name="add_problem")
]