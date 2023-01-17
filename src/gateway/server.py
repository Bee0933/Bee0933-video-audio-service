import os, gridfs, pika, json
from pymongo import MongoClient
from fastapi import FastAPI, status, Depends, HTTPException, Security, File, UploadFile
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from auth import validate
from auth_svc import access
from storage import util
import uvicorn

server = FastAPI()
basic_auth = HTTPBasic()
security = HTTPBearer()

MONGO_URI = "mongodb://host.minikube.internal:27017/videos"

mongo = MongoClient(MONGO_URI)

fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


# login route
@server.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: HTTPBasicCredentials = Depends(basic_auth)):
    token, err = access.login(credentials=credentials)
    if not err:
        return token
    message, stats = err[0], err[1]
    raise HTTPException(status_code=stats, detail=message)


# upload file route
@server.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(
    auth_credentials: HTTPAuthorizationCredentials = Security(security),
    file: UploadFile = File(description="upload and read file"),
):
    usr_access, err = validate.token(auth_credentials)

    usr_access = json.loads(usr_access)

    if usr_access["admin"]:
        if err := util.upload(file, fs, channel, usr_access):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err
            )

        return "succcess!"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized user"
        )


# download mp3 route
@server.get("/download", status_code=status.HTTP_200_OK)
async def download():
    pass


if __name__ == "__main__":
    uvicorn.run(app=server, host="0.0.0.0", port=8002)
