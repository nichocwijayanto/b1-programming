import hashlib

class User:
    def __init__(self, username, password, privilege_level, login_attempt=0, account_status="Active"):
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters.")
        if not isinstance(password, str):
            raise TypeError("Password must be a string.")
        if len(password) < 9:
            raise ValueError("Password must be at least 8 characters.")
        if not isinstance(privilege_level, str):
            raise TypeError("Privilege level must be a string.")
        
        self.username = username
        self.__hashed_password = self.__hash_password(password)
        self.__set_privilege_level(privilege_level)
        self.__login_attempt = login_attempt
        self.__account_status = account_status
        self.__log_list = []

    # Hash password input
    def __hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Verify password input hash, with hashed password 
    def __verify_password(self, password):
        return self.__hash_password(password) == self.__hashed_password

    def __set_privilege_level(self, privilege_level):
        allowed_level = ['admin', 'standard', 'guest']
        if privilege_level not in allowed_level:
            raise ValueError("Privilege level does not exist.")
        self.__privilege_level = privilege_level
    
    def __log_record(self, message):
        self.__log_list.append(message)

    def __lock_account(self):
        self.__account_status = "LOCKED"

    def authenticate(self, username, password):
        if self.__account_status == "LOCKED":
            return False
        if self.__verify_password(password): 
            self.__login_attempt = 0
            self.__log_record(f"Loggin Successful! - User: {username}")
            return True
        else:
            self.__login_attempt += 1
            if self.__login_attempt == 3:
                self.__lock_account()
                #log_activity record failed attempt.
                self.__log_record(f"Loggin FAILED!! - User: {username} has {self.__login_attempt} login attempts.")
                return False

    def check_privileges(self, required_level):
        self.required_level = required_level
        level = {
            'admin': 3,
            'standard': 2,
            'guest': 1
        }
        user_level = level.get(self.__privilege_level, 0) #__set_privilege_level(), returns Integer from level dictionary.
        required_level = level.get(required_level, 0)     # returns Integer from level dictionary.

        self.__log_record(f"Access Check: {self.username}('{self.__privilege_level}') attempting '{self.required_level}' task.")

        if user_level >= required_level:
            self.__log_record(f"Access GRANTED for user ('{self.username}') with '{self.__privilege_level}' level accessing '{self.required_level}' level.")
            return True
        
        self.__log_record(f"Access DENIED for user ('{self.username}' with '{self.__privilege_level}' level accessing '{self.required_level})' level.")
        return False

    def get_privilege_level(self):
        return self.__privilege_level
    
    def get_user_info(self):
        return {
            "User": self.username,
            "Role": self.get_privilege_level(),
            "Status": self._User__account_status 
        }

users = [
    User("Alice", "SecurePass123", "guest"),
    User("Bob", "VeryStr0ngPass", "standard"),
    User("Mallory", "mypassword6767?", "admin")
]

print("\n=== Security Outcome: Input Validation ===")
try:
    bad_user = User("X", "short", "hacker")
except (ValueError, TypeError) as e:
    print(f"Blocked invaled user creation: {e}")

print("\n=== Security Outcome: Brute Force Prevention (Alice) ===")
for i in range(3):
    users[0].authenticate("Alice", "WrongPass")
print(f"Alice's current status: {users[0].get_user_info()['Status']}")

print("\n=== Security Outcome: Privilege Escalation Prevention ===")
print(f"Alice (Guest) accessing Admin level: {users[0].check_privileges('admin')}")
print(f"Mallory (Admin) accessing Standard level: {users[2].check_privileges('standard')}")

print("\n=== Security Outcome: Encapsulation Check ===")
try:
    print(users[1].__hashed_password)
except AttributeError:
    print("Success: Private attribute '__hashed_password' is hidden from external access.")

print("\n=== Final Audit Log (Mallory) ===")
for entry in users[2]._User__log_list:
    print(f"> {entry}")
print("\n")