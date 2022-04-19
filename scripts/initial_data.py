import requests
from pygradus import create_exercise, check_solution

data = {"username": "admin", "password": "admin"}
r = requests.post("http://0.0.0.0:8000/users/", data=data)

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


result = create_exercise("admin", config, url="http://0.0.0.0:8000")
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

result = create_exercise("admin", config, url="http://0.0.0.0:8000")
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
check_solution(proposed_solution)


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
check_solution(proposed_solution)

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
check_solution(proposed_solution)
