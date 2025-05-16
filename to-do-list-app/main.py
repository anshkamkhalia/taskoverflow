from flask import Flask, render_template, request, redirect, url_for
from task import Task
import json
import os

app = Flask(__name__)
TASK_FILE = "tasks.json"

# Reads the task
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Save all
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Gets tasks from user, saves it, and then returns it back to template
@app.route("/", methods=["GET", "POST"])
def home():
    tasks = load_tasks()

    # New Task
    if request.method == "POST":

        task_name = request.form.get("task")

        if task_name:

            new_task = Task(name=task_name, completed=False)

            tasks.append({
                "name": new_task.name,
                "date": new_task.date,
                "completed": new_task.completed
            })
            save_tasks(tasks)

        # Redirecting
        return redirect(url_for("home"))
    
    # Rendering template
    return render_template("index.html", tasks=tasks)

# Checkboxes
@app.route("/toggle/<int:index>", methods=["POST"])
def toggle(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        # Get the current 'completed' status of the task at the given index (default to False if missing)
        current_status = tasks[index].get("completed", False)
        
        # Toggle the 'completed' status: if True, set to False; if False, set to True
        tasks[index]["completed"] = not current_status
        
        # Save the updated tasks list back to the storage (e.g., JSON file)
        save_tasks(tasks)
    
    return redirect(url_for("home"))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)