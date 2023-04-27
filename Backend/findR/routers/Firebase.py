import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins="*",
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

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
def add_user(first_name: str, last_name: str,username: str, password: str, email: str):
    # Check if the user already exists
    print(first_name, last_name,username, password, email)
    existing_user = ref.child('users').order_by_child('username').equal_to(username).get()
    for user_key, user_val in existing_user.items():
        if user_val.get('password') == password:
            return {"message": "User already exists"}

    # Insert the user into the database
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "password": password,
        "email": email,

    }
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

# Endpoint for checking username and password
@app.get('/login')
def check_login(username: str, password: str):
    all_users = ref.child('users').get()
    if all_users:
        for u in all_users.values():
            if u.get('username') == username and u.get('password') == password:
                return {'message': 'Login successful'}
    raise HTTPException(status_code=401, detail='Invalid credentials')

@app.post("/clear")
def clear_collection():
    """Clears all data from the database."""
    ref.delete()