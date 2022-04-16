# ===================================================={ all imports }============================================================

from fastapi.testclient import TestClient
from typing import List, Dict

from code.main import app
from code.database import get_db

from code import models
from code import crud

# ==================================================={ global objects }==========================================================

client = TestClient(app)

USERNAME = "test@gmail.com"
PASSWORD = "test"

ANSWER = "test answer"

NAME = "test"

# ====================================================={ login test }============================================================


def get_token(username: str, password: str):
    response = client.post("/token/", data={"username": username, "password": password})
    if response.status_code == 200:
        return f"Bearer {response.json()['access_token']}"
    else:
        return None


# ================================================={ create new user test }======================================================


def create_new_user(username: str, password: str):
    response = client.post("/users/", data={"username": username, "password": password})
    assert response.status_code == 200
    session = next(get_db())
    user = crud.get_user_by_email(session, username)
    assert user.username == username


# ================================================{ create new course test }======================================================


def create_new_course(token: str, name: str):
    response = client.post(
        "/course/",
        json={"name": name},
        headers={"Authorization": token},
    )
    assert response.status_code == 200
    session = next(get_db())
    crud.get_course(session, name)


# ==============================================={ create new exercise test }=====================================================


def create_new_exercise(token: str, name: str, course_name: str):
    response = client.post(
        "/exercise/",
        json={"name": name, "course_name": course_name},
        headers={"Authorization": token},
    )
    assert response.status_code == 200
    session = next(get_db())
    crud.get_exercise(session, name, course_name)


# ================================================{ create new task test }========================================================


def create_new_task(
    token: str, name: str, answer: str, exercise_name: str, course_name: str
):

    data = {
        "name": name,
        "answer": answer,
        "exercise_name": exercise_name,
        "course_name": course_name,
        "disabled": False,
    }

    response = client.post(
        "/task/",
        json=data,
        headers={"Authorization": token},
    )
    assert response.status_code == 200
    session = next(get_db())
    crud.get_task(session, name, exercise_name, course_name)


# # ==============================================={ create new attempt test }======================================================


def create_new_attempt(
    username: str,
    exercise_name: str,
    course_name: str,
    answers: List[Dict[str, str]],
):

    attempt = {
        "attempt": {
            "username": username,
            "exercise_name": exercise_name,
            "course_name": course_name,
        },
        "task_attempts": answers,
    }

    response = client.post("/attempt/", json=attempt)
    assert response.status_code == 200
    return response.json()


def delete_current_user(token: str) -> None:

    response = client.delete("/users/", headers={"Authorization": token})
    assert response.status_code == 200


def get_student_results(student_name: str, course_name: str):

    response = client.get(f"/results/{course_name}/{student_name}")
    assert response.status_code == 200
    return response.json()


def get_instructor_results(token: str, course_name: str):

    response = client.get(
        f"/results/{course_name}",
        headers={
            "Authorization": token,
        },
    )
    assert response.status_code == 200
    return response.json()


# =====================


def test_create_user_with_one_tasks():

    username = "test@gmail.com"
    password = "password"
    course_name = "new_course"
    exercise_name = "new_exercise"
    task_name = "new_task"
    task_answer = "42"

    student_name = "student"
    student_answers = [{"name": task_name, "answer": "50"}]

    create_new_user(username, password)
    token = get_token(username, password)
    create_new_course(token, course_name)
    create_new_exercise(token, exercise_name, course_name)
    create_new_task(token, task_name, task_answer, exercise_name, course_name)

    attempt = create_new_attempt(
        student_name, exercise_name, course_name, student_answers
    )
    assert attempt["total_correct"] == 0

    try:
        create_new_course(token, course_name)
        assert 0  # course exists
    except AssertionError:
        assert "Course Exists, not created"

    student_answers_2 = [{"name": task_name, "answer": "42"}]
    attempt = create_new_attempt(
        student_name, exercise_name, course_name, student_answers_2
    )
    assert attempt["total_correct"] == 1

    delete_current_user(token)

    session = next(get_db())
    # import pdb

    # pdb.set_trace()
    for model in [
        models.User,
        models.Course,
        models.Exercise,
        models.Task,
        models.Attempt,
    ]:

        print(model)
        count = session.query(model).count()
        assert count == 0


def test_get_student_results():

    username = "test@gmail.com"
    password = "password"
    course_name = "new_course"
    exercise_name_a = "exercise_a"
    exercise_name_b = "exercise_b"
    task_a_1 = "a_1"
    task_a_1_answer = "a_1"
    task_b_1 = "b_1"
    task_b_1_answer = "b_1"
    task_b_2 = "b_2"
    task_b_2_answer = "b_2"

    create_new_user(username, password)
    token = get_token(username, password)
    create_new_course(token, course_name)
    create_new_exercise(token, exercise_name_a, course_name)
    create_new_exercise(token, exercise_name_b, course_name)
    create_new_task(token, task_a_1, task_a_1_answer, exercise_name_a, course_name)
    create_new_task(token, task_b_1, task_b_1_answer, exercise_name_b, course_name)
    create_new_task(token, task_b_2, task_b_2_answer, exercise_name_b, course_name)

    student_name = "alice"
    student_answers = [{"name": task_a_1, "answer": "incorrect"}]
    attempt = create_new_attempt(
        student_name, exercise_name_a, course_name, student_answers
    )
    assert attempt["total_correct"] == 0

    student_answers = [
        {
            "name": task_b_1,
            "answer": "incorrect",
        },
        {
            "name": task_b_2,
            "answer": "b_2 inc",
        },
    ]
    attempt = create_new_attempt(
        student_name, exercise_name_b, course_name, student_answers
    )
    assert attempt["total_correct"] == 0

    student_answers = [
        {
            "name": task_b_1,
            "answer": "incorrect",
        },
        {
            "name": task_b_2,
            "answer": "b_2",
        },
    ]
    attempt = create_new_attempt(
        student_name, exercise_name_b, course_name, student_answers
    )
    assert attempt["total_correct"] == 1

    student_results = get_student_results(student_name, course_name)
    assert student_results == {
        "exercise_a": {"correct": 0, "total": 1},
        "exercise_b": {"correct": 1, "total": 2},
    }


def test_get_student_result_2():

    course_name = "new_course"
    exercise_name_a = "exercise_a"
    exercise_name_b = "exercise_b"
    task_a_1 = "a_1"
    task_a_1_answer = "a_1"
    task_b_1 = "b_1"
    task_b_1_answer = "b_1"
    task_b_2 = "b_2"
    task_b_2_answer = "b_2"

    student_name = "bob"
    student_answers = [{"name": task_a_1, "answer": "incorrect 1"}]
    attempt = create_new_attempt(
        student_name, exercise_name_a, course_name, student_answers
    )
    assert attempt["total_correct"] == 0

    student_answers = [{"name": task_a_1, "answer": "incorrect 2"}]
    attempt = create_new_attempt(
        student_name, exercise_name_a, course_name, student_answers
    )
    assert attempt["total_correct"] == 0

    student_results = get_student_results(student_name, course_name)
    assert student_results == {
        "exercise_a": {"correct": 0, "total": 1},
        "exercise_b": {"correct": 0, "total": 2},
    }

    student_answers = [{"name": task_a_1, "answer": "a_1"}]
    attempt = create_new_attempt(
        student_name, exercise_name_a, course_name, student_answers
    )
    assert attempt["total_correct"] == 1

    student_results = get_student_results(student_name, course_name)
    assert student_results == {
        "exercise_a": {"correct": 1, "total": 1},
        "exercise_b": {"correct": 0, "total": 2},
    }


def test_results_instructor():

    username = "test@gmail.com"
    password = "password"
    course_name = "new_course"

    token = get_token(username, password)
    results = get_instructor_results(token, course_name)
    assert results == {
        "alice": {
            "exercise_a": {"correct": 0, "total": 1},
            "exercise_b": {"correct": 1, "total": 2},
        },
        "bob": {
            "exercise_a": {"correct": 1, "total": 1},
            "exercise_b": {"correct": 0, "total": 2},
        },
    }
