import requests
from getpass import getpass

def build_exercise(username, config, url="https://notebook-grading.herokuapp.com"):

    #password = getpass()
    password = "12345"
    headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(
        url + "/token",
        headers=headers,
        data={"username": username, "password": password}
    )
    if r.status_code == 200:
        token = f"Bearer {r.json()['access_token']}"
    else:
        raise Exception(r.text)
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": token
    }
    
    # Get existing user data
    r = requests.get(
        url + "/users/me",
        headers=headers,
    )
    if r.status_code == 200:
        user_data = r.json()
    else:
        raise Execption("Failed to get user data")

    course = config["course_name"]
    my_course = {}
    for c in user_data["courses"]:
        if course == c["name"]: # the course is already mine
            my_course = c
            break
    else:
        r = requests.post(
            url + "/course/",
            headers=headers,
            json={"name": course},
        )
        if r.status_code != 200:
            return r.text
        
        my_course = r.json()
    
    exercise = config["exercise_name"]
    data = {"course_name": course, "name": exercise}
    my_exercise = {}
    for ex in my_course["exercises"]:
        if exercise == ex["name"]:
            my_exercise = ex
            break
    else:
        r = requests.post(
            url + "/exercise",
            headers=headers,
            json=data
        )
        if r.status_code != 200:
            return r.text

    tasks = config["tasks"]
    my_tasks = my_exercise["tasks"]
    data = {"course_name": course, "exercise_name": exercise}
    for t in tasks:
        r = requests.post(
            url + "/task",
            headers=headers,
            json={
                **data,
                **t,
                "disabled": False,
            }
        )
        if r.status_code != 200:
            return r.text

    # disable missing tasks
    new_tasks_names = [t["name"] for t in tasks]
    for t in my_tasks:
        if t["name"] not in new_tasks_names:
            print(t)
            r = requests.post(
                url + "/task",
                headers=headers,
                json={
                    **t,
                    "disabled": True,
                }
            )
            if r.status_code != 200:
                return r.text


    r = requests.get(
        url + "/users/me",
        headers=headers,
    )
    if r.status_code == 200:
        user_data = r.json()
    else:
        return r.text
    
    return user_data