from db import Sessionlocal, user, create_db
import os, datetime, jwt
from fastapi import FastAPI, status, Depends, Security
from fastapi.security import (
    HTTPBasicCredentials,
    HTTPBasic,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
import uvicorn


server = FastAPI()
basic_auth = HTTPBasic()
security = HTTPBearer()



# @server.on_event("startup")
# def create_postgres_orm():
#     create_db()


# Dependency
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# test route
@server.get("/test", status_code=status.HTTP_200_OK)
async def login(db: Session = Depends(get_db)):
    new_user = user(email='best@mail.com', password='pass')
    db.add(new_user)
    db.commit()
    return 'populate test user'


@server.post("/login", status_code=status.HTTP_201_CREATED)
async def login(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="missing credentials"
        )
    db_user = db.query(user).filter(user.email == credentials.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user does not exist"
        )
    if str(db_user.password) != str(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect password"
        )
    else:
        # return createJWT(credentials.username, 'secret', True)
        return createJWT(credentials.username, os.environ.get("JWT_SECRET"), True)


def createJWT(username: str, secret: str, authz: bool):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


@server.post("/validate", status_code=status.HTTP_200_OK)
async def validate(credentials: HTTPAuthorizationCredentials = Security(security)):
    encoded_jwt = credentials.credentials
    if not encoded_jwt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="missing credentials"
        )
    try:
        decoded = jwt.decode(
            # encoded_jwt, 'secret', algorithm=["HS256"]
            encoded_jwt,
            os.environ.get("JWT_SECRET"),
            algorithm=["HS256"],
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized"
        ) from exc

    return decoded


if __name__ == "__main__":
    uvicorn.run(app=server, host="0.0.0.0", port=8001)
