import requests
import secrets
import hashlib
 
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
 
def main():
    base_url = "http://script:6000" # the URL of the database API
    auth_client = AuthClient(base_url)
   
    while True:
        print("\nChoose an option:")
        print("1. Register")
        print("2. Login")
        print("3. Unregister")
        print("4. Exit")
       
        choice = input("\nEnter your choice (1-4): ")
       
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            if auth_client.register(username, password, email):
                print(f"Registered user: {username}")
       
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if auth_client.login(username, password):
                print(f"Logged in successfully as: {username}")
                print(f"Token: {auth_client.token}")
                
                # access the interpreter API
                interpreter_url = "http://compiler:8000"
                while True:
                    print("\nChoose an option:")
                    print("1. Execute code")
                    print("2. Logout")
                   
                    choice = input("\nEnter your choice (1-2): ")
                   
                    if choice == "1":
                        code = input("Enter code: ")
                        url = f"{interpreter_url}/interpreter"
                        data = {"code": code}
                        headers = {"Authorization": f"Bearer {auth_client.token}"}
                        response = requests.post(url, json=data, headers=headers)
                        if response.status_code == 200:
                            result = response.text
                            if result == 'Unauthorized access':
                                print("Unauthorized access. Please login first.")
                            else:
                                print(f"Result: {result}")
                        else:
                            print(f"Error {response.status_code}: {response.text}")
                       
                    elif choice == "2":
                        auth_client.logout()
                        print("Logged out successfully.")
                        break
                   
                    else:
                        print("Invalid choice. Please enter either 1 or 2.")
            else:
                print("Invalid username-password combination.")
       
        elif choice == "3":
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            if auth_client.unregister(username, password, email):
                print(f"Successfully unregistered user: {username}")
       
        elif choice == "4":
            print("Exiting...")
            break
       
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == '__main__':
    main()