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
 
if __name__ == '__main__':
    # base_url = "http://127.0.0.1:25000" # url-ul database API
    base_url = "http://script:6000" # url-ul database API
    #IMPORTANT DE VAZUT CARE I ADRESA#
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
            else:
                print("Invalid username-password combination.")
       
        elif choice == "3":
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            if auth_client.unregister(username, password, email):
                print(f"Unregistered user: {username}")
       
        elif choice == "4":
            print("Exiting...")
            break
       
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")