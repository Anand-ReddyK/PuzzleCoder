from django.db import models
from Database.base_model import BaseCollection
# Create your models here.

class codingProblem(BaseCollection):

    def __init__(self):
        super().__init__("codingproblems", use_custom_id=True)

codingProblem = codingProblem()

class User(BaseCollection):
    def __init__(self):
        super().__init__("users")

User = User()

class UserProblemsData(BaseCollection):
    def __init__(self):
        super().__init__("userproblemdata")

UserProblemsData = UserProblemsData()