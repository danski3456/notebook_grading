
#===================================================={ all imports }============================================================

from fastapi.testclient import TestClient

from code.main import app
#==================================================={ global objects }==========================================================

client = TestClient(app)

TEST_USERNAME = 'test@gmail.com'
TEST_PASSWORD = 'test'

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
        print('New user created:', response.json().get("username"))
    else:
        print('Error creating user:', response.json())

#================================================{ create new course test }======================================================

def create_new_course(name:str):
    result = token(TEST_USERNAME, TEST_PASSWORD)
    if not result:
        print ('Error getting token')
        return
    response = client.post('/course/', json={"name":name}, headers={"Authorization": "Bearer " + result.get("access_token")})
    if response.status_code == 200:
        print('New course created:', response.json().get("name"))
    else:
        print('Error creating course:', response.json())

#==============================================={ create new exercise test }=====================================================

def create_new_exercise(name:str, course_name:str):
    result = token(TEST_USERNAME, TEST_PASSWORD)
    if not result:
        print ('Error getting token')
        return
    
    response = client.post('/exercise/', 
                           json={"name":name, "course_name": course_name},
                           headers={"Authorization": "Bearer " + result.get("access_token")}
                           )
    if response.status_code == 200:
        print('New exercise created:', response.json().get("name"))
    else:
        print('Error creating exercise:', response.json())

#==============================================={ create new attempt test }======================================================

def create_new_attempt(exercise_name:str, course_name:str, answer:str, name:str):
    
    attempt = {
        "attempt": {
            "username": TEST_USERNAME,
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
        print('New attempt created:', response.json())
    else:
        print('Error creating attempt:', response.json())


#====================================================={ main part }==============================================================

if __name__ == '__main__':
    print('Automated test started')
    create_new_user(TEST_USERNAME, TEST_PASSWORD)
    print()
    create_new_course('Test course')
    print()
    create_new_exercise('Test exercise', 'Test course')
    print()
    create_new_attempt('Test exercise', 'Test course', 'Test answer', 'Test name')
    
#===================================================={ code ends here }==========================================================
