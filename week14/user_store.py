# handles data (files)
import json
import os

class UserStore:
    def __init__(self, file_path):
        self.file_path = file_path

# use print statements to verify your logic works correctly.

    # returns a list of user dictionaries
    def load(self):
        if not os.path.exists(self.file_path):
            print(f"DEBUG: File '{self.file_path}' not found. Returning empty list.")
            return []
    
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                # converts texts inside into a Python list for manipulation. 
                print(f"DEBUG: Successfully loaded {len(data)} users from '{self.file_path}'.")
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"DEBUG: Error loading file: {e}. Returning empty list.")
            return []

    # writes users as JSON lines
    def save(self, users):
        with open(self.file_path, "w") as f:
            json.dump(users, f, indent=4) 
            print(f"DEBUG: Data successfully saved to '{self.file_path}'. Total users: {len(users)}.")

    # returns user dict or None
    def find_by_id(self, id):
        print(f"DEBUG: Searching for user with ID: {id}")
        users = self.load()

        for user in users:
            if user['id'] == id:
                print(f"DEBUG: Found user: {user['name']}")
                return user

        print(f"DEBUG: User with ID {id} not found.")
        return None

    # Figures out what the next ID should be (ID 1, 2, etc.)
    def get_next_id(self, users):
        # checks if list is empty. 
        if not users:
            return 1 # if empty, return 1 bcs the first person in the database should be User #1.
        
        # finds the highest ID user in the list and add 1 for the next one. 
        return max(user['id'] for user in users) + 1

    def search(self, q):
        users = self.load()
        
        # logic: keep the user IF the letter {variable q} is inside their name. -> doesn't have to be full username.
        results = [u for u in users if q.lower() in u['name'].lower()]
        return results
    
    def update_user(self, id, updated_data):
        users = self.load()
    
        for user in users:
            if user['id'] == id:
                user['name'] = updated_data.name
                user['email'] = updated_data.email
                self.save(users)  # save the changes to the file.
                return user
        
        return None

    def delete_user(self, id):
        users = self.load()
        
        new_users = [u for u in users if u['id'] != id]

        if len(new_users) < len(users): 
            self.save(new_users)  
            return True
        return False    # return False if the ID wasn't found. 
    
    def add_user(self, user_in):
        users = self.load()

        new_user = {
            "id": self.get_next_id(users),
            "name": user_in.name,
            "email": user_in.email
        }

        users.append(new_user)
        self.save(users)
        return new_user