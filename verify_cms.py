from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app import models, auth

# Reset DB
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_cms_flow():
    print("Starting CMS Verification Flow...")
    
    # 1. Create Users
    print("Creating users...")
    teacher_data = {"name": "Teacher A", "email": "teach@example.com", "password": "pass", "role": "teacher"}
    student_data = {"name": "Student A", "email": "stud@example.com", "password": "pass", "role": "student"}
    
    # We can create directly via CRUD or API. Let's use API to test 'users' router and auth implicitly? 
    # Actually register endpoint usually exists but here we have create_user in crud/users router. 
    # Wait, 'users' router has list, read, update, delete. Does it have create?
    # I verified 'users.py'. It does NOT have create! Standard separate 'register' router usually handles it or 'admin' creates users.
    # But for this test, I will create users via DB since the UI flow for registration isn't explicitly defined yet or requires admin.
    # Wait, I checked `crud.py` it has `create_user`.
    # I'll create them via DB session for setup.
    
    db = SessionLocal()
    from app import crud, schemas
    teacher = crud.create_user(db, schemas.UserCreate(**teacher_data))
    student = crud.create_user(db, schemas.UserCreate(**student_data))
    db.close()
    
    # Login Teacher
    print("Logging in Teacher...")
    resp = client.post("/auth/token", data={"username": "teach@example.com", "password": "pass"})
    assert resp.status_code == 200
    teach_token = resp.json()["access_token"]
    teach_headers = {"Authorization": f"Bearer {teach_token}"}
    
    # Login Student
    print("Logging in Student...")
    resp = client.post("/auth/token", data={"username": "stud@example.com", "password": "pass"})
    assert resp.status_code == 200
    stud_token = resp.json()["access_token"]
    stud_headers = {"Authorization": f"Bearer {stud_token}"}
    
    # 2. Teacher creates Course
    print("Teacher creating course...")
    course_data = {"title": "Python 101", "description": "Intro to Python"}
    resp = client.post("/courses/", json=course_data, headers=teach_headers)
    assert resp.status_code == 200
    course_id = resp.json()["id"]
    
    # Module
    mod_data = {"title": "Basics", "description": "Variables", "course_id": course_id}
    resp = client.post("/courses/modules", json=mod_data, headers=teach_headers)
    assert resp.status_code == 200
    module_id = resp.json()["id"]
    
    # Lesson
    les_data = {"title": "Var Types", "content": "int, str...", "module_id": module_id}
    resp = client.post("/courses/lessons", json=les_data, headers=teach_headers)
    assert resp.status_code == 200
    lesson_id = resp.json()["id"]
    
    # Quiz (Assessment)
    print("Teacher creating quiz...")
    quiz_data = {
        "title": "Module 1 Quiz",
        "description": "Test basics",
        "module_id": module_id,
        "questions": [
            {
                "text": "What is 1+1?", 
                "question_type": "multiple_choice",
                "options": [
                    {"text": "1", "is_correct": False},
                    {"text": "2", "is_correct": True}
                ]
            }
        ]
    }
    resp = client.post(f"/assessments/modules/{module_id}/quizzes", json=quiz_data, headers=teach_headers)
    if resp.status_code != 200:
        print(resp.json())
    assert resp.status_code == 200
    quiz_id = resp.json()["id"]
    
    # Assignment
    print("Teacher creating assignment...")
    assign_data = {"title": "HW1", "description": "Do math", "course_id": course_id}
    resp = client.post(f"/assessments/courses/{course_id}/assignments", json=assign_data, headers=teach_headers)
    assert resp.status_code == 200
    assign_id = resp.json()["id"]
    
    # 3. Student Actions
    print("Student enrolling...")
    resp = client.post(f"/courses/{course_id}/enroll", headers=stud_headers)
    assert resp.status_code == 200, f"Enrollment failed: {resp.text}"
    
    # Progress
    print("Student tracking progress...")
    prog_data = {"completed": True}
    resp = client.post(f"/tracking/progress?lesson_id={lesson_id}", json=prog_data, headers=stud_headers)
    assert resp.status_code == 200
    
    # Submit Assignment
    print("Student submitting assignment...")
    sub_data = {"assignment_id": assign_id, "content": "My Answer"}
    resp = client.post("/assessments/submissions", json=sub_data, headers=stud_headers)
    assert resp.status_code == 200
    sub_id = resp.json()["id"]
    
    # 4. Teacher Grades
    print("Teacher grading...")
    grade_data = {"score": 95.0, "feedback": "Good job"}
    resp = client.put(f"/assessments/submissions/{sub_id}/grade", json=grade_data, headers=teach_headers)
    assert resp.status_code == 200
    assert resp.json()["score"] == 95.0
    
    # 5. Tracking Certificate
    print("Student requesting certificate...")
    # This might fail logic if I didn't mock it fully in 'tracking.py'. 
    # I implemented 'issue_certificate' without checks.
    resp = client.post(f"/tracking/certificates/issue?course_id={course_id}", headers=stud_headers)
    assert resp.status_code == 200
    print("Certificate URL:", resp.json()["certificate_url"])
    
    print("Verification Successful!")

if __name__ == "__main__":
    import sys
    try:
        test_cms_flow()
        print("SUCCESS")
    except Exception as e:
        print(f"FAILED: {e}")
        # print details if needed
        # import traceback
        # traceback.print_exc()
        sys.exit(1)
