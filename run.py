try:
    from app import create_app, db
    
    app = create_app()
    
    if __name__ == '__main__':
        print("🚀 Flask 앱을 시작합니다...")
        with app.app_context():
            db.create_all()
            print("✅ 데이터베이스 생성 완료")
        
        print("🌐 서버 시작: http://127.0.0.1:5000")
        app.run(debug=True, host='127.0.0.1', port=5000)
        
except Exception as e:
    print(f"❌ 에러 발생: {e}")
    import traceback
    traceback.print_exc()
