from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-key-123'

@app.route('/test')
def test():
    return 'Flask is working!'

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Hospital Management System API'}

if __name__ == '__main__':
    print("Starting test server...")
    print("Visit: http://127.0.0.1:5000/test")
    print("Visit: http://127.0.0.1:5000/health")
    app.run(debug=True, port=5000)
