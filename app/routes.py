from flask import (
    Flask,
    render_template,
    request
)
from datetime import datetime
import requests

app = Flask(__name__)
BACKEND_URL = 'http://127.0.0.1:5000'



@app.get("/")
def home():
    mylist = [1, 2, 3, 4, 5]
    timestamp = datetime.now().strftime("%F %H:%M:%S")
    return render_template('home.html', ts=timestamp, numbers=mylist)

@app.get("/about")
def about():
    return render_template('about.html')

@app.get("/tasks")
def list_tasks():
    url = "%s/tasks" % BACKEND_URL
    response = requests.get(url)
    if response.status_code == 200:
        task_list = response.json().get('tasks')
        return render_template("task_list.html", tasks=task_list)
    return render_template(
        "error.html", err=response.status_code), response.status_code

@app.get("/task/edit/<int:pk>")
def render_edit_form(pk):
    url = "%s/tasks/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("edit.html", task=task_data)
    return render_template(
        "error.html", err=response.status_code), response.status_code

@app.post("/tasks/edit/<int:pk>")
def update_task(pk):
    url = "%s/tasks/%s" % (BACKEND_URL, pk)
    task_data = request.form
    response = requests.put(url, json=task_data)
    if response.status_code == 204:
        return render_template("success.html")
    return render_template(
        "error.html", response.status_code), response.status_code

@app.get("/tasks/new")
def render_new_form():
    return render_template("new.html")

@app.post("/task/new")
def create_task():
    pass

@app.get("/tasks/<int:pk>")
def view_task_by_id(pk):
    url = "%s/tasks/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("detail.html", task=task_data)
    return render_template(
        "error.html", err=response.status_code), response.status_code
