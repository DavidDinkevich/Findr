import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from fastapi import FastAPI, HTTPException

app = FastAPI()

path = "credentials\privateAccountKey.json"
cred = credentials.Certificate(path)

firebase_admin.initialize_app(cred, {'databaseURL': 'https://findr-78bed-default-rtdb.firebaseio.com'})

# Get a reference to the root node of your database
ref = db.reference('/')


@app.get("/")
def health_check():
    return {"status":"healthy"}

@app.get("/users/{username}")
def get_user(username: str):
    user = ref.child('users').child(username).get()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/")
def add_user(username: str, age: int):
    # Check if the user already exists
    existing_user = ref.child('users').child(username).get()
    if existing_user is not None:
        return {"error": "User already exists"}

    # Insert the user into the database
    user = {"username": username, "age": age}
    ref.child('users').child(username).set(user)
    return {"message": "User added to database"}

@app.get("/all_users")
def get_all_users():
    users = []
    all_users = ref.child('users').get()
    if all_users:
        for username, user in all_users.items():
            users.append(user)
    return users

@app.put("/users/{username}")
def update_user(username: str, age: int = None):
    try:
        db = ref.child('users')
        # Find the user with the given username
        query = db.order_by_child('username').start_at(username)
        results = query.get()

        # Check if the user exists
        if not results:
            raise HTTPException(status_code=404, detail="User not found")

        # Update the user object with the new data
        for user_id, user_data in results.items():
            user_data['age'] = age
            db.child(user_id).set(user_data)

        # Return a success message
        return {"message": "User updated successfully"}

    except HTTPException as e:
        # Re-raise the HTTPException if the user is not found
        raise e

    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
def clear_collection():
    """Clears all data from the database."""
    ref.delete()