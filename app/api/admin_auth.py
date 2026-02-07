from fastapi import Header, HTTPException, status
import os

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

def admin_auth(x_admin_token: str = Header(...)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token"
        )
