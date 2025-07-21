from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    print("📱 Flask 앱 생성 중...")
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 모델 import 추가
    from . import models
    
    # Blueprint 등록 (임시 주석처리)
    # from .routes import api_bp
    # app.register_blueprint(api_bp)
    
    #@app.route('/')
    def home():
        return jsonify({
            "message": "🥮 붕어빵 시스템이 정상적으로 실행중입니다!",
            "api_docs": "/api",
            "version": "1.0.0"
        })
    
    print("✅ Flask 앱 생성 완료!")
    return app
