# import jwt
# from datetime import datetime, timedelta
# from fastapi import HTTPException

# SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWxpY2UiLCJleHAiOjE3NDgzMDg2MjR9.1q7wgWLi_-s_TL9f_P-k_MVYIgGlYHiNSNPnxv83210"

# def create_token(user_id: str):
#     payload = {
#         "user_id": user_id,
#         "exp": datetime.utcnow() + timedelta(hours=1)
#     }
#     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return payload["user_id"]
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")

import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = os.environ.get("SECRET_KEY", "your-super-secret-key")
ALGORITHM = "HS256"

def create_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)  # 1 day expiry
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

