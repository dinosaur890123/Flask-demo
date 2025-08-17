from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
app = Flask(__name__)
todos = []
DATA_FILE ='todos.json'
def load_todos():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        initial_todos = {}
        save_todos(initial_todos)
        return initial_todos
def save_todos(todos):
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f, indent=4)
@app.route('/')
def home():
    todos = load_todos()
    priority_map = {"High": 1, "Medium": 2, "Low": 3}
    sorted_todos = sorted(todos, key=lambda x: priority_map.get(x.get('priority'), 3))
    return render_template('index.html', todos=sorted_todos)

@app.route('/add', methods=['POST'])
def add_task():
    todos = load_todos()
    new_task_text = request.form.get('task_name')
    new_task_priority = request.form.get('task_priority')
    new_task_due_date = request.form.get('task_due_date')
    if new_task_text:
        new_task = {
            "text": new_task_text,
            "priority": new_task_priority,
            "due_date": new_task_due_date
        }
        todos.append(new_task)
        save_todos(todos)
    return redirect(url_for('home'))

@app.route('/edit/<int:task_index>', methods=['GET', 'POST'])
def edit_task(task_index):
    todos = load_todos()
    priority_map = {"High": 1, "Medium": 2, "Low": 3}
    sorted_todos = sorted(todos, key=lambda x: priority_map.get(x.get('priority'), 3))
    if not (0 <= task_index < len(sorted_todos)):
        flash('Invalid task', 'error')
        return redirect(url_for('home'))
    task_to_edit_sorted = sorted_todos[task_index]
    original_task = next((task for task in todos if task == task_to_edit_sorted), None)
    if request.method == 'POST':
        original_task['text'] = request.form.get('task_text')
        original_task['priority'] = request.form.get('priority')
        original_task['due_date'] = request.form.get('due_date')
        save_todos(todos)
        flash('Task success')
        return redirect(url_for('home'))
    else:
        return render_template('edit.html', task=original_task, task_index=task_index)

@app.route('/delete/<int:task_index>')
def delete_task(task_index):
    todos = load_todos()
    priority_map = {"High": 1, "Medium": 2, "Low": 3}
    sorted_todos = sorted(todos, key=lambda x: priority_map.get(x.get('priority'), 3))

    if 0 <= task_index < len(sorted_todos):
        task_to_remove = sorted_todos[task_index]
        todos.remove(task_to_remove)
        save_todos(todos)
        flash('Task deleted') 
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)