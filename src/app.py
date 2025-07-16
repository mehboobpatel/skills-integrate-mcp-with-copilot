"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""


from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
import json
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# Add session middleware for login sessions
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

# Load teacher credentials from JSON file
TEACHERS_FILE = os.path.join(current_dir, "teachers.json")
def load_teachers():
    with open(TEACHERS_FILE, "r") as f:
        return json.load(f)

def is_teacher_logged_in(request: Request):
    return request.session.get("teacher_username") is not None

def require_teacher(request: Request):
    if not is_teacher_logged_in(request):
        raise HTTPException(status_code=401, detail="Teacher login required.")

# Login endpoint
@app.post("/login")
async def login(request: Request, credentials: dict):
    username = credentials.get("username")
    password = credentials.get("password")
    teachers = load_teachers()
    for teacher in teachers:
        if teacher["username"] == username and teacher["password"] == password:
            request.session["teacher_username"] = username
            return {"message": "Login successful", "username": username}
    raise HTTPException(status_code=401, detail="Invalid credentials.")

# Logout endpoint
@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}

# Check login status
@app.get("/login-status")
async def login_status(request: Request):
    username = request.session.get("teacher_username")
    return {"logged_in": bool(username), "username": username}

# Load teacher credentials from JSON file
TEACHERS_FILE = os.path.join(current_dir, "teachers.json")
def load_teachers():
    with open(TEACHERS_FILE, "r") as f:
        return json.load(f)

def is_teacher_logged_in(request: Request):
    return request.session.get("teacher_username") is not None

def require_teacher(request: Request):
    if not is_teacher_logged_in(request):
        raise HTTPException(status_code=401, detail="Teacher login required.")

# Login endpoint
@app.post("/login")
async def login(request: Request, credentials: dict):
    username = credentials.get("username")
    password = credentials.get("password")
    teachers = load_teachers()
    for teacher in teachers:
        if teacher["username"] == username and teacher["password"] == password:
            request.session["teacher_username"] = username
            return {"message": "Login successful", "username": username}
    raise HTTPException(status_code=401, detail="Invalid credentials.")

# Logout endpoint
@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}

# Check login status
@app.get("/login-status")
async def login_status(request: Request):
    username = request.session.get("teacher_username")
    return {"logged_in": bool(username), "username": username}

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, request: Request = None):
    """Sign up a student for an activity (teacher only)"""
    require_teacher(request)
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, request: Request = None):
    """Unregister a student from an activity (teacher only)"""
    require_teacher(request)
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
