from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)
todos = []
DATA_FILE ='todos.json'
@app.route('/')
def load_todos():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_todos = ["Do this", "Do that", "Do something"]
        save_todos(default_todos)
        return default_todos
def save_todos(todos):
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f)


def home():
    todos = load_todos()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('task_name')
    if new_task:
        todos.append(new_task)
    return redirect(url_for('home'))


@app.route('/delete/<int:task_index>')
def delete_task(task_index):
    if 0 <= task_index < len(todos):
        todos.pop(task_index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)