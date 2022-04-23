import requests
from pygradus import create_exercise, check_solution

url = "http://0.0.0.0:8000"

data = {"username": "admin", "password": "admin"}
r = requests.post(url + "/users/", data=data)

if r.status_code == 200:
    print("User created correctly")

tasks = [
    {
        "name": "remove_vowels",
        "answer": "hl cm sts",
    },
    {
        "name": "sum_floats",
        "answer": "[1, 2, 3]",
    },
]
config = {
    "course_name": "first-course",
    "exercise_name": "first-exercise",
    "tasks": tasks,
}


result = create_exercise("admin", config, url=url)
print("First exercise", result)

tasks = [
    {
        "name": "simple",
        "answer": "not so simple",
    },
]
config = {
    "course_name": "first-course",
    "exercise_name": "second-exercise",
    "tasks": tasks,
}

result = create_exercise("admin", config, url=url)
print("Second exercise", result)


##### Creating attempts by users


## Exercise 1
proposed_solution = {
    "attempt": {
        "course_name": "first-course",
        "exercise_name": "first-exercise",
        "username": "student-1",
    },
    "task_attempts": [
        {
            "name": "remove_vowels",
            "answer": "cm sts",
        },
        {
            "name": "sum_floats",
            "answer": "[2, 3]",
        },
    ],
}
result = check_solution(proposed_solution, url=url)
print(result)


## Exercise 2
proposed_solution = {
    "attempt": {
        "course_name": "first-course",
        "exercise_name": "second-exercise",
        "username": "student-1",
    },
    "task_attempts": [
        {
            "name": "simple",
            "answer": "nanan",
        },
    ],
}
result = check_solution(proposed_solution, url=url)
print(result)

proposed_solution = {
    "attempt": {
        "course_name": "first-course",
        "exercise_name": "second-exercise",
        "username": "student-1",
    },
    "task_attempts": [
        {
            "name": "simple",
            "answer": "not so simple",
        },
    ],
}
result = check_solution(proposed_solution, url=url)
print(result)
