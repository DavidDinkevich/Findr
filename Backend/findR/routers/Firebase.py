import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from fastapi import FastAPI, HTTPException,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import routers.model_requests as ML_R
from controller_utils import *
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

firebase_url = 'https://findr-78bed-default-rtdb.firebaseio.com'
firebase_admin.initialize_app(cred, {'databaseURL': firebase_url})

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
def add_user(full_name: str, username: str, password: str, email: str):
    # Check if the user already exists
    existing_user = ref.child('users').order_by_child('username').equal_to(username).get()
    for user_key, user_val in existing_user.items():
        if user_val.get('password') == password:
            return {"message": "User already exists"}

    # Insert the user into the database
    user = {
        "full_name": full_name,
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


# Endpoint for checking username and password
@app.get('/login')
def check_login(username: str, password: str):
    all_users = ref.child('users').get()
    if all_users:
        for u in all_users.values():
            if u.get('username') == username and u.get('password') == password:
                return {'message': 'Login successful'}
    raise HTTPException(status_code=401, detail='Invalid credentials')

#endpoint to return user results to FE
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
    processed_results = process_results(response)
    seconds_response = frames_to_seconds(processed_results[0],json.loads(response)['num_frames'],duration)
    processed = processed_results[1]
    return str(seconds_response) + '&' +str(processed)

'''
Returns all the algorithms that user chose
'''
def get_options_list(options):
    return [element.strip() for element in options.split(',')]

@app.post("/clear")
def clear_collection():
    """Clears all data from the database."""
    ref.delete()