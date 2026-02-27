# This file is where all the action happens (for a user). 
from fastapi import APIRouter, HTTPException
from schema import User, UserCreate     # imports from file schema.py the class User & UserCreate
from user_store import UserStore

'''
Decorators (@) only live here. --> They are "Web Address" signs, that tell FastAPI which URL leads to which function.

'''

# 'router' acts like a mini-app ('Department Manager') just for user tasks.
router = APIRouter()    # handles web traffic (URLs). 

store = UserStore("users.db")  # the routes talk to the store via this object.

# POST /users - Create a new user
# bcs of prefix="/users" on 'main.py', no need to type /users anymore. It's glued to the front of it already. 
@router.post("/", response_model=User)  #-> .post() -> send data. Turns the code to a URL instead of normal function. 
def create_user_endpoint(user_in: UserCreate):
    return store.add_user(user_in)

# GET /users - Get the full list
@router.get("/", response_model=list[User]) #-> .get() -> get/retrieve data.
def get_all_users_endpoint():
    return store.load()

# GET /users/search - Search by name
# IMPORTANT: This MUST come before the /{id} route!
@router.get("/search", response_model=list[User])
def search_user_endpoint(q: str):
    return store.search(q)

# GET /users/id
@router.get("/{id}", response_model=User)
def get_user_by_id_endpoint(id: int):    # Type hint. Validation & Casting. 
    return store.find_by_id(id)

# PUT /users/id
@router.put("/{id}", response_model=User)
def update_user_endpoint(id: int, user_update: UserCreate):
    updated_user = store.update_user(id, user_update)
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# DELETE /users/id
@router.delete("/{id}")
def delete_user_endpoint(id: int):
    success = store.delete_user(id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}