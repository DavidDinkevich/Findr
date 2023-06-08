import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from fastapi import FastAPI, HTTPException,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import routers.model_requests as ML_R
from utils import *
from moviepy.editor import VideoFileClip

import aiofiles
import os

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

@app.post("/uploadfile/{query}/{options}")
async def create_upload_file(options :str, query:str,file: UploadFile = File(...)):
    options_list = get_options_list(options)
    print(options_list)
    contents = await file.read()  # binary read
    # Save file to disk
    filename = file.filename
    async with aiofiles.open(filename, 'wb') as f:
        await f.write(contents)
    clip = VideoFileClip(os.path.abspath(filename))
    duration = clip.duration
    response = ML_R.send_request(query,os.path.abspath(filename),options_list)
    seconds_response = frames_to_seconds(get_first_interval_values(response),json.loads(response)['num_frames'],duration)
    return str(seconds_response) + '&' +str(response)
    #Return response with saved file
    # file_path = os.path.abspath(filename)
    # return FileResponse(file_path, media_type="video/mp4", filename=filename)

def get_options_list(options):
    return [element.strip() for element in options.split(',')]
@app.post("/clear")
def clear_collection():
    """Clears all data from the database."""
    ref.delete()