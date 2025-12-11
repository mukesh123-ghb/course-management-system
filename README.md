# Course Management System (CMS)

A full-featured **Course Management System (CMS)** built with **FastAPI**, supporting course creation, assessments, user roles, content delivery, progress tracking, and administrative tools.

---

## 🚀 Features

### **1. Course Creation & Management**

* Create and organize courses
* Upload multimedia content (PDFs, videos, presentations)
* Lesson planning and structuring
* Syllabus management

### **2. User Management**

* Student and instructor authentication
* Role-based access control (Admin / Teacher / Student)
* User grouping by departments, batches, and classes

### **3. Content Delivery**

* Access online learning resources
* Interactive lessons (videos, quizzes, text modules)
* Forums and discussion channels
* Announcements and notifications

### **4. Assessment & Evaluation**

* Auto-graded quizzes
* Assignments with grading and feedback
* Exam scheduling and basic proctoring support
* Student progress tracking

### **5. Communication Tools**

* Internal messaging system
* Forums, discussion boards
* Email and notification system
* Integrated live classes (Zoom/Teams-ready)

### **6. Tracking & Reporting**

* Student performance reports
* Attendance tracking
* Course analytics dashboard
* Downloadable certificates

### **7. Administrative Features**

* Course catalog management
* Scheduling and calendar
* Payment support (if needed)
* Compliance-ready structure

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **Database:** SQLite / PostgreSQL
* **ORM:** SQLAlchemy
* **Auth:** OAuth2 + JWT
* **Environment:** Python 3.x

---

## 📁 Project Structure

```
course_management_system/
│
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── database.py            # DB configuration
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── crud.py                # Database operations
│   ├── auth.py                # Authentication logic
│   ├── dependencies.py        # Dependencies injection
│   │
│   ├── routers/               # Route handlers
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── courses.py
│   │   ├── lessons.py
│   │   ├── assessments.py
│   │   ├── tracking.py
│   │   ├── notifications.py
│   │   ├── forum.py
│   │   └── users.py
│
├── requirements.txt
├── reset_db.py
├── verify_cms.py
└── .gitignore
```

---

## ⚙️ Installation & Setup

### **Clone the Repository**

```bash
git clone https://github.com/Malikabriq/course-management-system.git
cd course-management-system
```

### **Create Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Run the Server**

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📌 API Documentation

FastAPI automatically generates interactive docs:

* **Swagger UI:** `/docs`
* **ReDoc:** `/redoc`

---

## 📝 License

This project is licensed under the **MIT License**.

---

## 🤝 Contributions

Contributions are welcome! Feel free to fork the repo and open pull requests.

---

## ⭐ Support

If you like this project, give it a **star** on GitHub!
