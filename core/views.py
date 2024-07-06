from django.shortcuts import render, HttpResponse
from .models import codingProblem
import json
from bson.objectid import ObjectId
# Create your views here.


def problems_page(request):
    problems = codingProblem.find_all({"_id": 1, "title": 1, "difficulty": 1})
    context = {"problem_data": problems}

    return render(request, "core/home.html", context)



def add_problem(request):
    problem = [{
    "title": "Climbing Stairs",
    "description": {
      "problem": "You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
      "examples": [
        {
          "input": "n = 2",
          "output": "2",
          "description": "There are two ways to climb to the top: 1 step + 1 step, 2 steps."
        },
        {
          "input": "n = 3",
          "output": "3",
          "description": "There are three ways to climb to the top: 1 step + 1 step + 1 step, 1 step + 2 steps, 2 steps + 1 step."
        }
      ],
      "function_description": {
        "inputs": [
          {
            "name": "n",
            "type": "int",
            "description": "The total number of steps."
          }
        ],
        "returns": {
          "type": "int",
          "description": "The number of distinct ways to reach the top."
        }
      },
      "input_format": "An integer n representing the total number of steps.",
      "constraints": [
        {
          "constraint": "1 <= n <= 45"
        }
      ],
      "sample_input_output": [
        {
          "input": "2",
          "expected_output": "2"
        }
      ],
      "test_cases": [
        {
          "input": "2",
          "expected_output": "2"
        },
        {
          "input": "3",
          "expected_output": "3"
        }
      ]
    }
  }
]
    
    a = codingProblem.insert(problem)
    return HttpResponse(f"Data Inserted {str(a)}")