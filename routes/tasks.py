from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Task, Category, StatusEnum, PriorityEnum

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())  
    data = request.json
    task = Task(
        title=data['title'],
        status=StatusEnum[data.get('status', 'pending')],
        priority=PriorityEnum[data.get('priority', 'medium')],
        user_id=user_id,
        category_id=data.get('category_id')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created'})

@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())  
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'status': t.status.value,
        'priority': t.priority.value,
        'created_at': t.created_at,
        'category': t.category.name if t.category else None
    } for t in tasks])

@tasks_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.json
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created'})
