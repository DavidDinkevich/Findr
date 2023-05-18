import uvicorn


from routers.Firebase import app

if __name__ == "__main__":
    print("running server")
    print(f"----------- PORT: {5002}")
    uvicorn.run(app,host = '127.0.0.1',port = 5002)