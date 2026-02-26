import json
import os
from fastapi import APIRouter, HTTPException
from schema import User, UserCreate

# 'router' acts like a mini-app just for user tasks.
router = APIRouter()

# database file
DB_FILE = "users.txt"

# Reads text file and turns it into Python list.
def read_users():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        try:
            # converts texts inside into a Python list for manipulation. 
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Takes the list of users and saves it back to the text file.
def write_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)   # takes python list and dumps it as JSON format. 

# Figures out what the next ID should be (ID 1, 2, etc.)
def get_next_id(users):
    # checks if list is empty. 
    if not users:
        return 1    # if empty, return 1 bcs the first person in the database should be User #1.
    
    # finds the highest ID user in the list and add 1 for the next one. 
    return max(user['id'] for user in users) + 1

# POST /users - Create a new user
@router.post("/", response_model=User)  #-> .post() -> send data. Turns the code to a URL instead of normal function. 
def create_user(user_in: UserCreate):
    users = read_users()                # grab current list from text file.
    
    new_user = {
        "id": get_next_id(users),       # assign them a new ID number.
        "name": user_in.name,           # take name from the request.
        "email": user_in.email          # take email from the request.
    }

    users.append(new_user)              # (?) add them to python list. 
    write_users(users)                  # overwrite the text file with the updated list.
    return new_user                     # send new user back to the screen.

# GET /users - Get the full list
@router.get("/", response_model=list[User]) #-> .get() -> get/retrieve data.
def get_all_users():
    return read_users()

# GET /users/search - Search by name
# IMPORTANT: This MUST come before the /{id} route!
@router.get("/search", response_model=list[User])
def search_users(q: str):
    users = read_users()    # get everyone
    # logic: keep the user IF the letter {variable q} is inside their name"
    results = [u for u in users if q.lower() in u['name'].lower()]
    return results

@router.get("/{id}", response_model=User)
def get_user_by_id(id: int):
    users = read_users()

    for user in users:
        if user['id'] == id:
            return user

    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{id}", response_model=User)
def update_user(id: int, user_update: UserCreate):
    users = read_users()
    
    for user in users:
        if user['id'] == id:
            user['name'] = user_update.name
            user['email'] = user_update.email
            write_users(users)  # save the changes to the file.
            return user
    
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{id}")
def delete_user(id: int):
    users = read_users()

    # create a new list that includes everyone EXCEPT the person we want to delete.
    new_users = [u for u in users if u['id'] != id]

    if len(new_users) == len(users):     # (?) LOGIC???
        raise HTTPException(status_code=404, detail="User not found")
    
    write_users(new_users)  # save the shorter list
    return {"message": "User deleted successfully"}