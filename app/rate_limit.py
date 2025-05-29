from fastapi import Request, HTTPException
from time import time

RATE_LIMIT = 5
TIME_WINDOW = 60  # seconds
clients = {}

async def rate_limiter(request: Request):
    ip = request.client.host
    now = time()
    history = clients.get(ip, [])
    history = [t for t in history if now - t < TIME_WINDOW]
    if len(history) >= RATE_LIMIT:
        raise HTTPException(429, detail="Too Many Requests: Slow down!")
    history.append(now)
    clients[ip] = history
