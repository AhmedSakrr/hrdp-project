# file name : main.py
# path : /hrdpflask/main.py


from app import create_app

# 여기서 생성해서
app = create_app()

if __name__ == '__main__':
    app.run()(debug=True, host='0.0.0.0')
