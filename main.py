from database import SessionLocal
from models import User as UserModel
from fastapi import FastAPI
from pydantic import BaseModel
from auth import hash_password, verify_password, create_access_token
from pydantic import ConfigDict

app = FastAPI()


#@app.get("/")
#def home():
#   return {"message": "My API is alive!"}


# @app.get("/hello/{name}")
#def greet(name: str):
 #   return {"message": f"Hello {name}!"} 
    


#@app.get("/add")
#def add(a: int, b: int):
 #   return {"result": a + b}


class User(BaseModel):
    name: str
    age: int
    email: str
    password: str
users = []



class UserOut(BaseModel):
    id: int
    name: str
    age: int
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)

#@app.post("/users")
#def create_user(user: User):
#    users.append(user)
#    return {"message": f"Created user {user.name}, age {user.age}"}
@app.post("/users")
def create_user(user: User):
    db = SessionLocal()
    new_user = UserModel(name=user.name, age=user.age, email=user.email, hashed_password=hash_password(user.password))
    
    db.add(new_user)
    db.commit()
    return {"message": f"Created user {new_user.name}, age {new_user.age}"}


#@app.get("/users")
#def list_users():
#   return users


@app.get("/users", response_model=list[UserOut])
def list_users():
    db = SessionLocal()
    return db.query(UserModel).all()


#@app.put("/users/{user_id}")
#def update_user(user_id: int, user: User):
#    if user_id < 0 or user_id >= len(users):
#        return {"error": "User not found"}
#    users[user_id] = user
#    return {"message": f"Updated user {user_id} to {user.name}, age {user.age}"}


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    db = SessionLocal()
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if db_user is None:
        return {"error": "User not found"}

    db_user.name = user.name
    db_user.age = user.age
    db.commit()

    return {"message": f"Updated user {user_id} to {user.name}, age {user.age}"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if db_user is None:
        return {"error": "User not found"}
    
    db.delete(db_user)  
    db.commit()  
    
    return {"message": f"Deleted user {db_user.name}"}
#@app.delete("/users/{user_id}")
#def delete_user(user_id: int):
#    if user_id < 0 or user_id >= len(users):
#       return {"error": "User not found"}
#   removed = users.pop(user_id)
#    return {"message": f"Deleted user {removed.name}"}


@app.post("/login")
def login(email: str, password: str):
    db = SessionLocal()
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    
    if db_user is None:
        return {"error": "User not found"}
    
    if verify_password(password, db_user.hashed_password):
        token = create_access_token(db_user.email)
        return {"access_token": token, "token_type": "bearer"}
    else:
        return {"error": "Passwords do not match"}
    