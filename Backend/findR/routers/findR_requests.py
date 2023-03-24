from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

app = FastAPI()

# Connect to the default MongoDB instance on the local machine
client = MongoClient()

# Get a reference to the database
db = client.my_database

# Get a reference to the collection
collection = db.my_collection


def clear_collection(del_collection):
    """Clears all documents from the collection."""
    del_collection.delete_many({})

@app.get("/")
def health_check():
    return {"status":"healthy"}

@app.get("/users/{username}")
def get_user(username: str):
    user = collection.find_one({"username": username}, {"_id": False})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/")
def add_user(username: str, age: int):
    # Check if the user already exists
    existing_user = collection.find_one({"username": username}, {"_id": False})
    if existing_user is not None:
        return {"error": "User already exists"}

    # Insert the user into the collection
    user = {"username": username, "age": age}
    result = collection.insert_one(user)
    return {"message": "User added to database", "id": str(result.inserted_id)}

@app.get("/all_users")
def get_all_users():
    users = []
    for user in collection.find({},{"_id": False}):
        users.append(user)
    return users