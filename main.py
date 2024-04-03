from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)

employees = []

def basic_auth(username, password):
    return username == 'caio_ramos' and password == 'jose123'


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not basic_auth(auth.username, auth.password):
            return jsonify({'message': 'Authentication Failed. Please provide a valid username and password'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/employees', methods=['POST'])
@auth_required
def add_employee():
    employee_data = request.get_json()
    employees.append(employee_data)
    return jsonify({'message': 'Successfully added employee'}), 201

@app.route('/api/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

if __name__ == '__main__':
    app.run(debug=True)
