from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
todos = []
@app.route('/')
def home():
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