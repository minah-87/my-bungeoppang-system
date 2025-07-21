from flask import Blueprint, request, jsonify
from .services import (
    create_user, create_store, register_employee,
    get_all_users, get_all_stores, get_all_employees
)

# Blueprint 생성
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/')
def welcome():
    """API 환영 메시지"""
    return jsonify({
        "message": "🥮 붕어빵 시스템 API에 오신 것을 환영합니다!",
        "endpoints": {
            "users": {
                "POST /api/users/signup": "사용자 생성",
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

# 사용자 관련 API
@api_bp.route('/users/signup', methods=['POST'])
def signup_user():
    """사용자 회원가입"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "데이터가 제공되지 않았습니다"}), 400
    
    response, status = create_user(data)
    return jsonify(response), status

@api_bp.route('/users', methods=['GET'])
def list_users():
    """모든 사용자 조회"""
    users = get_all_users()
    return jsonify({
        "message": "사용자 목록 조회 성공",
        "users": users, 
        "count": len(users)
    })

# 가게 관련 API
@api_bp.route('/stores', methods=['POST'])
def create_store_route():
    """가게 생성"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "데이터가 제공되지 않았습니다"}), 400
    
    response, status = create_store(data)
    return jsonify(response), status

@api_bp.route('/stores', methods=['GET'])
def list_stores():
    """모든 가게 조회"""
    stores = get_all_stores()
    return jsonify({
        "message": "가게 목록 조회 성공",
        "stores": stores,
        "count": len(stores)
    })

# 직원 관련 API
@api_bp.route('/employees', methods=['POST'])
def register_employee_route():
    """직원 등록"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "데이터가 제공되지 않았습니다"}), 400
    
    response, status = register_employee(data)
    return jsonify(response), status

@api_bp.route('/employees', methods=['GET'])
def list_employees():
    """모든 직원 조회"""
    employees = get_all_employees()
    return jsonify({
        "message": "직원 목록 조회 성공",
        "employees": employees,
        "count": len(employees)
    })

