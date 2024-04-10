from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>----->' % self.id


@app.route('/', methods=['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        task_content = request.json.get('content', '').strip()
        if (task_content):
            new_task = Todo(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return jsonify({
                    'success': True,
                    'message': 'Task added successfully'
                })

            except:
                return jsonify({
                    'success': False,
                    'message': 'Content is required'
                })
        return jsonify({'success': False, 'message': 'Content is required'})

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    delete_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        })

    except:
        return jsonify({
            'success': False,
            'message': 'Content is not deleted'
        })


@app.route('/update/<int:id>', methods=['PATCH'])
def update(id):
    updateTask = Todo.query.get_or_404(id)
    data = request.json
    print(data, data['completed'])
    if ('content' in data):
        updateTask.content = data['content']
    elif ('completed' in data):
        updateTask.completed = data['completed']

    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'patching data',
        })
    except:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Content is not deleted'
        })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
