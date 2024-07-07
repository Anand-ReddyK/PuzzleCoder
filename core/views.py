from django.shortcuts import render, HttpResponse
from .models import codingProblem
import json
from bson.objectid import ObjectId
# Create your views here.


def problems_page(request):
    problems = codingProblem.find_all({"_id": 1, "title": 1, "difficulty": 1})
    context = {"problem_data": problems}

    return render(request, "core/problems.html", context)



def add_problem(request):
    problem = None
    a = codingProblem.insert(problem)
    return HttpResponse(f"Data Inserted {str(a)}")