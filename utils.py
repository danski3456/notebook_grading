import requests
from getpass import getpass
from IPython.nbformat import current as nbf
import re
from google.colab import _message


def build_exercise(username, config, url="https://notebook-grading.herokuapp.com"):

    password = getpass()
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
        my_exercise = r.json()

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


def check_solution(proposal, url="https://notebook-grading.herokuapp.com"):
    import requests
    r = requests.post(
        url + "/attempt/",
        json = proposal,
    )
    if r.status_code != 200:
        return r.text
    res = r.json() 

    max_len = 50
    answers = res["task_attempts"]
    title = f"Total Correct Answers {res['total_correct']} / {len(answers)}"
    row = f"|{{0:^{max_len}}}|{{1:^20}}|"
    sep = row.format("-" * max_len, "-" * 20)
    print(row.format("Task Name", "Status"))
    print(sep)
    print(sep)
    for a in answers:
        print(row.format(
            a["name"][:max_len], 
            "Correct" if a["is_correct"] else "Incorrect"))
        print(sep)




def build_student_version(course_name, exercise_name):
    

    start_re = re.compile("#sss")
    end_re = re.compile("#eee")
    delete_re = re.compile("#ddd")
    tasks_re = re.compile("^#ttt")

    raw = _message.blocking_request('get_ipynb', request='', timeout_sec=5)
    cells = raw["ipynb"]["cells"]

    nb = nbf.new_notebook()

    tasks_content = None
    new_cells = []
    for c in cells:
        src = c["source"]
        start = None
        end = None
        delete = False
        tasks = False
        for i, l in enumerate(src):
            if start_re.search(l):
                start = i
            if end_re.search(l):
                end = i
            if delete_re.search(l):
                delete = True
            if tasks_re.search(l):
                tasks = True

        if start is not None and end is not None:
            new_src = src[:start] + ["    # Write your code here\n"] + src[end + 1:]
        else:
            new_src = src

        if tasks:
            tasks_content = src

        #c["source"] = new_src
        if delete or tasks:
            pass
        elif c["cell_type"] == "markdown":
            cell = nbf.new_text_cell("markdown", new_src)
            new_cells.append(cell)
        elif c["cell_type"] == "code":
            cell = nbf.new_code_cell(new_src)
            new_cells.append(cell)

        
    tasks_content = "".join(tasks_content[1:]).replace("TASKS = ", "")
    submission = f"""

proposed_solution = {{
    'attempt': {{
        'course_name': COURSE_NAME,
        'exercise_name': EXERCISE_NAME,
        'username': STUDENT_NAME,
    }},
    'task_attempts': {tasks_content}

}}
check_solution(proposed_solution)
    """
    cell = nbf.new_code_cell(submission)
    new_cells.append(cell)


    nb['worksheets'].append(nbf.new_worksheet(cells=new_cells))

    with open(f'{course_name}_{exercise_name}.ipynb', 'w') as f:
            nbf.write(nb, f, 'ipynb')