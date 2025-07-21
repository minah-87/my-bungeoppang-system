from werkzeug.security import generate_password_hash
from .models import User, Store, Employee
from . import db
import random

def create_user(data):
    """사용자 생성"""
    try:
        # 이메일 중복 체크
        if User.query.filter_by(email=data['email']).first():
            return {"error": "이미 존재하는 이메일입니다"}, 400
        
        # 비밀번호 해시화
        hashed_password = generate_password_hash(data['password'])
        
        # 새 사용자 생성
        new_user = User(
            first_name=data.get('first_name'),
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_password,
            address=data.get('address'),
            contact=data.get('contact'),
            gender=data.get('gender')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return {
            "message": "사용자가 성공적으로 생성되었습니다",
            "user_id": new_user.id,
            "name": f"{new_user.first_name} {new_user.last_name}"
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"사용자 생성 실패: {str(e)}"}, 500

def create_store(data):
    """가게 생성"""
    try:
        new_store = Store(
            name=data['name'],
            address=data.get('address'),
            contact=data.get('contact')
        )
        
        db.session.add(new_store)
        db.session.commit()
        
        return {
            "message": "가게가 성공적으로 생성되었습니다",
            "store_id": new_store.id,
            "name": new_store.name
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"가게 생성 실패: {str(e)}"}, 500

def register_employee(data):
    """직원 등록"""
    try:
        # 사용자와 가게 존재 확인
        user = User.query.get(data['user_id'])
        store = Store.query.get(data['store_id'])
        
        if not user:
            return {"error": "존재하지 않는 사용자입니다"}, 404
        if not store:
            return {"error": "존재하지 않는 가게입니다"}, 404
        
        # 직원번호 생성 (100000~999999)
        employee_code = random.randint(100000, 999999)
        
        # 직원번호 중복 체크
        while Employee.query.filter_by(code=employee_code).first():
            employee_code = random.randint(100000, 999999)
        
        new_employee = Employee(
            code=employee_code,
            user_id=data['user_id'],
            store_id=data['store_id'],
            type=data['type']
        )
        
        db.session.add(new_employee)
        db.session.commit()
        
        return {
            "message": "직원이 성공적으로 등록되었습니다",
            "employee_id": new_employee.id,
            "employee_code": new_employee.code,
            "user_name": f"{user.first_name} {user.last_name}",
            "store_name": store.name
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"직원 등록 실패: {str(e)}"}, 500

def get_all_users():
    """모든 사용자 조회"""
    users = User.query.filter_by(is_active=True).all()
    return [{
        "id": user.id,
        "name": f"{user.first_name} {user.last_name}",
        "email": user.email,
        "contact": user.contact,
        "gender": user.gender.value if user.gender else None
    } for user in users]

def get_all_stores():
    """모든 가게 조회"""
    stores = Store.query.filter_by(is_active=True).all()
    return [{
        "id": store.id,
        "name": store.name,
        "address": store.address,
        "contact": store.contact
    } for store in stores]

def get_all_employees():
    """모든 직원 조회"""
    employees = Employee.query.filter_by(is_active=True).all()
    return [{
        "id": employee.id,
        "employee_code": employee.code,
        "user_name": f"{employee.user.first_name} {employee.user.last_name}",
        "store_name": employee.store.name,
        "position": employee.type.value
    } for employee in employees]
