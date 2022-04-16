
#===================================================={ all imports }============================================================

from fastapi.testclient import TestClient

from code.main import app
#==================================================={ global objects }==========================================================

client = TestClient(app)

USERNAME = 'test@gmail.com'
PASSWORD = 'test'

ANSWER = 'test answer'

NAME = 'test'

#====================================================={ login test }============================================================

def token(username:str, password:str):
    response = client.post("/token/", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()
    else:
        return False

#================================================={ create new user test }======================================================

def create_new_user(username:str, password:str):
    response = client.post("/users/", data={"username": username, "password": password})
    if response.status_code == 200:
        print('New user created with username:', response.json().get("username"))
    else:
        print('Error creating user:', response.json())

#================================================{ create new course test }======================================================

def create_new_course(name:str):
    result = token(USERNAME, PASSWORD)
    if not result:
        print ('Error getting token')
        return
    response = client.post('/course/', json={"name":name}, headers={"Authorization": "Bearer " + result.get("access_token")})
    if response.status_code == 200:
        print('New course created with name:', response.json().get("name"))
    else:
        print('Error creating course:', response.json())

#==============================================={ create new exercise test }=====================================================

def create_new_exercise(name:str, course_name:str):
    result = token(USERNAME, PASSWORD)
    if not result:
        print ('Error getting token')
        return
    
    response = client.post('/exercise/', 
                           json={"name":name, "course_name": course_name},
                           headers={"Authorization": "Bearer " + result.get("access_token")}
                           )
    if response.status_code == 200:
        print('New exercise created with name:', response.json().get("name"))
    else:
        print('Error creating exercise:', response.json())
        
#================================================{ create new task test }========================================================

def create_new_task(name:str, answer:str, exercise_name:str, course_name:str):
    result = token(USERNAME, PASSWORD)
    if not result:
        print ('Error getting token')
        return
    
    data = {
            "name":  name,
            "answer": answer,
            "exercise_name": exercise_name,
            "course_name": course_name,
            "disabled": False
            }
    
    response = client.post('/task/', 
                           json=data,
                           headers={"Authorization": "Bearer " + result.get("access_token")}
                           )
    if response.status_code == 200:
        print('New task created with name:', response.json().get("name"))
    else:
        print('Error creating task:', response.json())

#==============================================={ create new attempt test }======================================================

def create_new_attempt(exercise_name:str, course_name:str, answer:str, name:str):
    
    attempt = {
        "attempt": {
            "username": USERNAME,
            "exercise_name": exercise_name,
            "course_name": course_name
            },
        "task_attempts": [
            {
                "answer": answer,
                "name": name
                }
            ]
        }
    
    response = client.post('/attempt/', json=attempt)
    
    if response.status_code == 200:
        print('New attempt created with id:', response.json().get("id"))
    else:
        print('Error creating attempt:', response.json())

#====================================================={ main part }==============================================================

if __name__ == '__main__':
    print('=========== Automated test started===========')
    print()
    create_new_user(USERNAME, PASSWORD)
    print()
    create_new_course(NAME)
    print()
    create_new_exercise(NAME, NAME)
    print()
    create_new_task(NAME, ANSWER, NAME, NAME)
    print()
    create_new_attempt(NAME, NAME, ANSWER, NAME)
    print()
    print('========== Automated test completed ==========')
#===================================================={ code ends here }==========================================================
