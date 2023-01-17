import os, requests
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials


def token(auth_token: HTTPAuthorizationCredentials):
    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid credential"
        )

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": f"Bearer {auth_token}"},
        timeout=5,
    )

    if response.status_code == status.HTTP_200_OK:
        return response.text, None
    else:
        return None, (response.txt, response.status_code)
