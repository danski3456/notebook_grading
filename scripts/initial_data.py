import requests
from pygradus import create_exercise, check_solution

url = "http://0.0.0.0:8000"


# =========================== { create course owners } =====================================

# Jhon Doe
data = {"username": "john", "password": "doe"}
r = requests.post(url + "/users/", data=data)
if r.status_code == 200:
    print("User created correctly")

# Jane Doe
data = {"username": "jane", "password": "doe"}
r = requests.post(url + "/users/", data=data)
if r.status_code == 200:
    print("User created correctly")

# =========================== { create courses for jhon } =====================================

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


result = create_exercise("john", config, url=url)
print("First exercise - First Course - Jhon", result)

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

result = create_exercise("john", config, url=url)
print("Second exercise - First Course - John", result)


# Create second exercise for john


tasks = [
    {
        "name": "hard exercise",
        "answer": "1234",
    },
    {
        "name": "easy exercise",
        "answer": "4321",
    },
    {
        "name": "medium exercise",
        "answer": "hi&bye",
    },
]
config = {
    "course_name": "second-course",
    "exercise_name": "first-exercise",
    "tasks": tasks,
}

result = create_exercise("john", config, url=url)
print("First exercise - Second Course - John", result)


# =========================== { create courses for jane } =====================================


for j in range(5):
    tasks = [
        dict(name=f"task {i}", answer=f"answer {i}") for i in range(j * 2, (j + 1) * 2)
    ]
    config = {
        "course_name": "cool course",
        "exercise_name": f"{j} ex",
        "tasks": tasks,
    }

    result = create_exercise("jane", config, url=url)

##### Creating attempts by users

# =========================== { create attempts for jhon first course } =====================================

student_ids = ["s1", "s2", "s3", "s1", "s4"]
remove_vowels_props = ["correct", "not so much", "hl cm sts", "hl cm sts", "incorrect"]
sum_floats_props = ["[1, 2, 3]", "[1, 2, 3]", "[1, 2, 3]", "[1, 2]", "[3, 2, 1]"]

for si, rvp, sfp in zip(student_ids, remove_vowels_props, sum_floats_props):

    ## Exercise 1
    proposed_solution = {
        "attempt": {
            "course_name": "first-course",
            "exercise_name": "first-exercise",
            "username": si,
        },
        "task_attempts": [
            {
                "name": "remove_vowels",
                "answer": rvp,
            },
            {
                "name": "sum_floats",
                "answer": sfp,
            },
        ],
    }
    result = check_solution(proposed_solution, url=url)
    print(result)


student_ids = ["s1", "s2", "s1", "s1"]
simple_props = ["not so simple", "what", "incorrect", "not so simple"]

for si, sp in zip(student_ids, simple_props):

    ## Exercise 2
    proposed_solution = {
        "attempt": {
            "course_name": "first-course",
            "exercise_name": "second-exercise",
            "username": si,
        },
        "task_attempts": [
            {
                "name": "simple",
                "answer": sp,
            },
        ],
    }
    result = check_solution(proposed_solution, url=url)
    print(result)

# =========================== { create attempts for jhon second course } =====================================

student_ids = ["s1", "s1", "s2", "s3", "s4", "s5"]
easy_props = ["1111", "4321", "4321", "0", "0"]
hard_props = ["0", "0", "1234", "1234", "0"]
medium_props = ["hi&bye", "hi&bye", "aa", "hi&bye", "hi&bye"]

for si, ep, hp, mp in zip(student_ids, easy_props, hard_props, medium_props):

    proposed_solution = {
        "attempt": {
            "course_name": "second-course",
            "exercise_name": "first-exercise",
            "username": si,
        },
        "task_attempts": [
            {
                "name": "easy exercise",
                "answer": ep,
            },
            {
                "name": "hard exercise",
                "answer": hp,
            },
            {
                "name": "medium exercise",
                "answer": mp,
            },
        ],
    }
    result = check_solution(proposed_solution, url=url)
    print(result)

# =========================== { create attempts for jane first course } =====================================


for j in range(5):
    for student in range(7):

        task_attempts = [
            dict(
                name=f"task {i}",
                answer=f"answer {i if (student % 3 == 0) and (j % 2 == 0) else -1}",
            )
            for i in range(j * 2, (j + 1) * 2)
        ]

        proposed_solution = {
            "attempt": {
                "course_name": "cool course",
                "exercise_name": f"{j} ex",
                "username": f"student {student}",
            },
            "task_attempts": task_attempts,
        }
        result = check_solution(proposed_solution, url=url)
        print(result)
