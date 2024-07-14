from django.shortcuts import render, HttpResponse, redirect
from .models import codingProblem, User
import json
from bson.objectid import ObjectId
# Create your views here.

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if "user" in request.session:
            return func(request, *args, **kwargs)
        return redirect("login")
    return wrapper

@login_required
def problems_page(request):
    problems = codingProblem.find_all({"_id": 1, "title": 1, "difficulty": 1})
    context = {"problem_data": problems}

    return render(request, "core/problems.html", context)

@login_required
def problem_detail(request, id):
    problem = codingProblem.find_one({"_id": id})
    context = {"problem_data": problem}

    if request.method == "POST":
        print(request.POST)

    return render(request, "core/problem_detail.html", context)

@login_required
def add_problem(request):
    problem = None
    a = codingProblem.insert(problem)
    return HttpResponse(f"Data Inserted {str(a)}")

def login_view(request):
    context = {
        "page_type": "login"
    }
    if request.method == "POST":
        username = request.POST["username"]
        user = User.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
            request.session['user'] = user
            return redirect('problems_page')
        context["invalid"] = "User does not exist"
    
    return render(request, "core/auth.html", context)

def signup_view(request):
    context = {
        "page_type": "signup"
    }
    if request.method == "POST":
        username = request.POST["username"]
        user = User.find_one({"username": username})
        if not user:
            User.insert({"username": username})
            return redirect("problems_page")

        context["invalid"] = "User already exists"
    
    return render(request, "core/auth.html", context)

def code_view(request):
    if request.method == "POST":
        print(request.POST)
    
    return HttpResponse("sperrr")