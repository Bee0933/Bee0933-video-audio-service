import os, requests
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials


def login(credentials: HTTPBasicCredentials):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="invalid credentials"
        )

    auth_basic = (credentials.username, credentials.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=auth_basic, timeout=5
    )

    if response.status_code == status.HTTP_200_OK:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)
