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
    
    @app.route('/')
    def home():
        return jsonify({"message": "🥮 붕어빵 시스템 시작!"})
    
    print("✅ Flask 앱 생성 완료!")
    return app
