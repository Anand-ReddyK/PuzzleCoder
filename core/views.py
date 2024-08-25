from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import codingProblem, User, UserProblemsData
import json
from bson.objectid import ObjectId
from Redis_connection.redis_conn import enqueue_task, get_task_results
# Create your views here.

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if "user" in request.session:
            return func(request, *args, **kwargs)
        return redirect("login")
    return wrapper

def logout_view(request):
    del request.session["user"]
    return redirect("login")

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
            user = User.find_one({"username": username})
            user["_id"] = str(user["_id"])
            request.session['user'] = user
            return redirect("problems_page")

        context["invalid"] = "User already exists"
    
    return render(request, "core/auth.html", context)


@login_required
def problems_page(request):
    problems = list(codingProblem.find_all(projection={"_id": 1, "title": 1, "difficulty": 1}))
    result_status = list(UserProblemsData.find_all(query={"user_id": request.session["user"]["_id"]},
                                              projection={"_id": 0, "pass_rate": 1, "problem_id": 1}))
    
    results = {status["problem_id"]: status.get("pass_rate", -1) for status in result_status}
    
    for problem in problems:
        problem["pass_rate"] = results.get(problem["_id"], -1)

    context = {"problem_data": problems}

    return render(request, "core/problems.html", context)


@login_required
def problem_detail(request, id):
    problem = codingProblem.find_one({"_id": id})
    userCode = UserProblemsData.find_one({
        "user_id": request.session["user"]["_id"],
        "problem_id": id
    })

    # If the user already submitted the code for the probelm we are getting it.
    if userCode is not None:
        problem["user_language"] = userCode["language"]
        problem["run_code"][userCode["language"]] = userCode["code"]
    
    # Making it easy to format in the frontend
    problem["run_code"] = json.dumps(problem["run_code"])

    context = {"problem_data": problem}

    if request.method == "POST":
        print(request.POST)

    return render(request, "core/problem_detail.html", context)


@login_required
def add_problem(request):
    problem = None

    a = codingProblem.insert(problem)
    return HttpResponse(f"Data Inserted {str(a)}")


@require_POST
def submit_code(request, id):
    data = request.POST
    test_cases = codingProblem.find_one({"_id": id})["description"]["test_cases"]
    user_id = request.session["user"]["_id"]
    UserProblemsData.insert_or_update(
        data={
            "user_id": user_id,
            "problem_id": id,
            "code": data["code"],
            "language": data["language"]
        },
        projection={
            "user_id": user_id,
            "problem_id": id
        }
    )
    enqueue_task(data["language"], data["code"], test_cases, user_id, problem_id=id)
    return JsonResponse({"message":"Code Enqued"}, status=200)


def code_results(request):
    if request.method == "GET":
        user_id = request.session["user"]["_id"]
        result = get_task_results(user_id)
        if result == "Pending":
            return JsonResponse({"result": result}, status=202)

        UserProblemsData.update(projection={
            "user_id": user_id,
            "problem_id": result['problem_id']
        }, data={"pass_rate": result["pass_rate"]})
        return JsonResponse({"result": result}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)