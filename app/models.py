from datetime import datetime
from . import db
from enum import Enum

# Enum 정의
class GenderEnum(Enum):
    MALE = "남성"
    FEMALE = "여성"

class PositionEnum(Enum):
    MANAGER = "매니저"
    STAFF = "스태프"

# User 모델
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    contact = db.Column(db.String(50))
    gender = db.Column(db.Enum(GenderEnum), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    
    # 관계 설정
    employees = db.relationship('Employee', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

# Store 모델
class Store(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255))
    contact = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # 관계 설정
    employees = db.relationship('Employee', back_populates='store')
    
    def __repr__(self):
        return f'<Store {self.name}>'

# Employee 모델
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True, nullable=False)
    type = db.Column(db.Enum(PositionEnum), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # 외래키
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id', ondelete='CASCADE'), nullable=False)
    
    # 관계 설정
    user = db.relationship('User', back_populates='employees')
    store = db.relationship('Store', back_populates='employees')
    
    def __repr__(self):
        return f'<Employee {self.code}>'
