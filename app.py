from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"status": "QCam API is running"}

@app.get("/ping")
def ping():
    return JSONResponse({"pong": True})
