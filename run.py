from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from enum import Enum
import random

# 전역 객체 생성
db = SQLAlchemy()
migrate = Migrate()

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
    employees = db.relationship('Employee', backref='user', lazy=True)
    
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
    employees = db.relationship('Employee', backref='store', lazy=True)
    
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
    
    def __repr__(self):
        return f'<Employee {self.code}>'

def create_app():
    app = Flask(__name__)
    
    # 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bungeoppang.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'my-bungeoppang-secret-2024'
    app.config['DEBUG'] = True
    
    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 루트 라우트
    @app.route('/')
    def home():
        return jsonify({
            "message": "🥮 붕어빵 시스템이 정상적으로 실행중입니다!",
            "version": "2.0.0",
            "features": ["User Management", "Store Management", "Employee Management"],
            "endpoints": {
                "GET /": "홈페이지",
                "GET /api": "API 문서",
                "POST /api/users/signup": "사용자 가입",
                "GET /api/users": "사용자 목록",
                "POST /api/stores": "가게 생성",
                "GET /api/stores": "가게 목록",
                "POST /api/employees": "직원 등록",
                "GET /api/employees": "직원 목록"
            }
        })
    
    # API 홈
    @app.route('/api')
    def api_home():
        return jsonify({
            "message": "🥮 붕어빵 API v2.0",
            "description": "User, Store, Employee 관리 시스템",
            "endpoints": {
                "users": {
                    "POST /api/users/signup": "사용자 가입",
                    "GET /api/users": "사용자 목록 조회"
                },
                "stores": {
                    "POST /api/stores": "가게 생성",
                    "GET /api/stores": "가게 목록 조회"
                },
                "employees": {
                    "POST /api/employees": "직원 등록",
                    "GET /api/employees": "직원 목록 조회"
                }
            }
        })
    
    # 사용자 가입 API
    @app.route('/api/users/signup', methods=['POST'])
    def signup_user():
        data = request.get_json()
        if not data:
            return jsonify({"error": "데이터가 제공되지 않았습니다"}), 400
        
        try:
            # 필수 필드 확인
            required_fields = ['last_name', 'email', 'password', 'gender']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"{field} 필드가 필요합니다"}), 400
            
            # 이메일 중복 체크
            if User.query.filter_by(email=data['email']).first():
                return jsonify({"error": "이미 존재하는 이메일입니다"}), 400
            
            # 비밀번호 해시화
            hashed_password = generate_password_hash(data['password'])
            
            # 새 사용자 생성
            new_user = User(
                first_name=data.get('first_name', ''),
                last_name=data['last_name'],
                email=data['email'],
                password=hashed_password,
                address=data.get('address', ''),
                contact=data.get('contact', ''),
                gender=GenderEnum(data['gender'])
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({
                "message": "사용자가 성공적으로 생성되었습니다",
                "user_id": new_user.id,
                "name": f"{new_user.first_name} {new_user.last_name}".strip(),
                "email": new_user.email
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"사용자 생성 실패: {str(e)}"}), 500
    
    # 사용자 목록 조회
    @app.route('/api/users', methods=['GET'])
    def list_users():
        try:
            users = User.query.filter_by(is_active=True).all()
            user_list = [{
                "id": user.id,
                "name": f"{user.first_name} {user.last_name}".strip(),
                "email": user.email,
                "contact": user.contact,
                "gender": user.gender.value if user.gender else None,
                "address": user.address
            } for user in users]
            
            return jsonify({
                "message": "사용자 목록 조회 성공",
                "users": user_list,
                "count": len(user_list)
            })
        except Exception as e:
            return jsonify({"error": f"사용자 목록 조회 실패: {str(e)}"}), 500
    
    # 가게 생성 API
    @app.route('/api/stores', methods=['POST'])
    def create_store():
        data = request.get_json()
        if not data:
            return jsonify({"error": "데이터가 제공되지 않았습니다"}), 400
        
        try:
            # 필수 필드 확인
            if 'name' not in data:
                return jsonify({"error": "가게 이름이 필요합니다"}), 400
            
            new_store = Store(
                name=data['name'],
                address=data.get('address', ''),
                contact=data.get('contact', '')
            )
            
            db.session.add(new_store)
            db.session.commit()
            
            return jsonify({
                "message": "가게가 성공적으로 생성되었습니다",
                "store_id": new_store.id,
                "name": new_store.name,
                "address": new_store.address
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"가게 생성 실패: {str(e)}"}), 500
    
    # 가게 목록 조회
    @app.route('/api/stores', methods=['GET'])
    def list_stores():
        try:
            stores = Store.query.filter_by(is_active=True).all()
            store_list = [{
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "contact": store.contact
            } for store in stores]
            
            return jsonify({
                "message": "가게 목록 조회 성공",
                "stores": store_list,
                "count": len(store_list)
            })
        except Exception as e:
            return jsonify({"error": f"가게 목록 조회 실패: {str(e)}"}), 500
    
    # 직원 등록 API
    @app.route('/api/employees', methods=['POST'])
    def register_employee():
        data = request.get_json()
        if not data:
            return jsonify({"error": "데이터가 제공되지 않았습니다"}), 400
        
        try:
            # 필수 필드 확인
            required_fields = ['user_id', 'store_id', 'type']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"{field} 필드가 필요합니다"}), 400
            
            # 사용자와 가게 존재 확인
            user = User.query.get(data['user_id'])
            store = Store.query.get(data['store_id'])
            
            if not user:
                return jsonify({"error": "존재하지 않는 사용자입니다"}), 404
            if not store:
                return jsonify({"error": "존재하지 않는 가게입니다"}), 404
            
            # 직원번호 생성 (100000~999999)
            employee_code = random.randint(100000, 999999)
            
            # 직원번호 중복 체크
            while Employee.query.filter_by(code=employee_code).first():
                employee_code = random.randint(100000, 999999)
            
            new_employee = Employee(
                code=employee_code,
                user_id=data['user_id'],
                store_id=data['store_id'],
                type=PositionEnum(data['type'])
            )
            
            db.session.add(new_employee)
            db.session.commit()
            
            return jsonify({
                "message": "직원이 성공적으로 등록되었습니다",
                "employee_id": new_employee.id,
                "employee_code": new_employee.code,
                "user_name": f"{user.first_name} {user.last_name}".strip(),
                "store_name": store.name,
                "position": new_employee.type.value
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"직원 등록 실패: {str(e)}"}), 500
    
    # 직원 목록 조회
    @app.route('/api/employees', methods=['GET'])
    def list_employees():
        try:
            employees = Employee.query.filter_by(is_active=True).all()
            employee_list = [{
                "id": employee.id,
                "employee_code": employee.code,
                "user_name": f"{employee.user.first_name} {employee.user.last_name}".strip(),
                "store_name": employee.store.name,
                "position": employee.type.value,
                "user_email": employee.user.email
            } for employee in employees]
            
            return jsonify({
                "message": "직원 목록 조회 성공",
                "employees": employee_list,
                "count": len(employee_list)
            })
        except Exception as e:
            return jsonify({"error": f"직원 목록 조회 실패: {str(e)}"}), 500
    
    return app

# 앱 생성
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ 데이터베이스 및 테이블 생성 완료!")
        print("📊 테이블: users, stores, employees")
    
    print("🚀 붕어빵 관리 시스템 v2.0 시작!")
    print("🌐 서버: http://127.0.0.1:8000")
    print("📖 API 문서: http://127.0.0.1:8000/api")
    app.run(debug=True, host='0.0.0.0', port=8000)
