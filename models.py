from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import enum

db = SQLAlchemy()

class RoleEnum(enum.Enum):
    user = "user"
    admin = "admin"

class StatusEnum(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class PriorityEnum(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.user)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.pending)
    priority = db.Column(db.Enum(PriorityEnum), default=PriorityEnum.medium)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    user = db.relationship('User', backref='tasks')
    category = db.relationship('Category', backref='tasks')

