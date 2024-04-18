import requests
import secrets

class AuthClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def login(self, username, password):
        url = f"{self.base_url}/login"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        
        if response.json()["success"]:
            self.token = secrets.token_hex(16)
            return True
        else:
            return False

    def register(self, username, password, email):
        url = f"{self.base_url}/register"
        data = {"username": username, "password": password, "email": email}
        response = requests.post(url, json=data)
        return response.json()["success"]

    def unregister(self, username, password, email):
        url = f"{self.base_url}/unregister"
        data = {"username": username, "password": password, "email": email}
        response = requests.post(url, json=data)
        return response.json()["success"]
#response e un json cu succes: fals/true
if __name__ == '__main__':
    base_url = "http://localhost:5000" # url-ul database API/ de schimbat in url-ul adevarat
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
            else:
                print("Failed to register.")
        
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if auth_client.login(username, password):
                print(f"Logged in successfully as: {username}")
                print(f"Token: {auth_client.token}")
            else:
                print("Failed to login.")
        
        elif choice == "3":
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            if auth_client.unregister(username, password, email):
                print(f"Unregistered user: {username}")
            else:
                print("Failed to unregister.")
        
        elif choice == "4":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")