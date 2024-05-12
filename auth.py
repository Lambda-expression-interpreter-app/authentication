import requests
import secrets
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
base_url = "http://script:6000"  # URL of the database API
interpreter_url = "http://interpreter:8001"  # URL of the interpreter API
auth_client = None

def compute_hash(string):
    return hashlib.sha512(string.encode()).hexdigest()
 
class AuthClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
 
    def login(self, username, password):
        if self.token is not None:
            print("You are already logged in with a user. Please logout first.")
            return None
        
        url = f"{self.base_url}/login"
        data = {"username": compute_hash(username), "password": compute_hash(password)}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()["success"]
            match str(result):
                case 'True':
                    self.token = secrets.token_hex(16)    
                    return True
                case 'False':
                    return False
                case _:
                    print("Returned message: " + str(result)) # some other (unknown) error
                    return False
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
        
    def logout(self):
        if self.token is not None:
            self.token = None
        else:
            print("You are not logged in with any user.")
   
    def register(self, username, password, email):
        url = f"{self.base_url}/register"
        data = {"username": compute_hash(username), "password": compute_hash(password), "email": compute_hash(email)}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()["success"]
            if result != 'Success':
                print(result)
                return False
            return True
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
 
    def unregister(self, username, password, email):
        url = f"{self.base_url}/unregister"
        data = {"username": compute_hash(username), "password": compute_hash(password), "email": compute_hash(email)}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()["success"]
            if result != 'Success':
                print(result)
                return False
            return True
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
 
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    auth_client = AuthClient(base_url)
    if auth_client.register(username, password, email):
        return jsonify({"message": f"Registered user: {username}"}), 200
    else:
        return jsonify({"error": "Failed to register user"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    global auth_client
    auth_client = AuthClient(base_url)
    if auth_client.login(username, password):
        # Implement login logic
        # Use requests.post to make HTTP requests to the interpreter API
        return jsonify({"message": f"Logged in successfully as: {username}"}), 200
    else:
        return jsonify({"error": "Invalid username-password combination"}), 401

@app.route('/execute', methods=['POST'])
def execute():
    global auth_client
    if auth_client:
        data = request.json
        code = data.get('code')
        url = f"{interpreter_url}/interpreter"
        headers = {"Authorization": f"Bearer {auth_client.token}"}
        response = requests.post(url, data=code, headers=headers)
        if response.status_code == 200:
            result = response.text
            if result == 'Unauthorized access':
                return jsonify({"error": "Unauthorized access. Please login first."}), 401
            else:
                return jsonify({"result": result}), 200
        else:
            return jsonify({"error": f"Error {response.status_code}: {response.text}"}), 500
    else:
        return jsonify({"error": "Not logged in."}), 400

@app.route('/logout', methods=['POST'])
def logout():
    global auth_client
    if auth_client:
        auth_client.logout()
        return jsonify({"message": "Logged out successfully."}), 200
    else:
        return jsonify({"error": "Not logged in."}), 400

@app.route('/unregister', methods=['POST'])
def unregister():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    auth_client = AuthClient(base_url)
    if auth_client.unregister(username, password, email):
        return jsonify({"message": f"Successfully unregistered user: {username}"}), 200
    else:
        return jsonify({"error": "Failed to unregister user"}), 400

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("Shutting down server...")
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)