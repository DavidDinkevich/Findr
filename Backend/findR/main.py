import uvicorn
from routers.Firebase import app

PORT=5002
if __name__ == "__main__":
    print("running server")
    print(f"----------- PORT: {PORT}")
    uvicorn.run(app,host = '127.0.0.1',port = PORT)