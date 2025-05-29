from fastapi import FastAPI, Depends, Request, HTTPException, Header
from app.validation import ChurnInput
from app.predict import predict_churn
from app.jwt import verify_token
from app.rate_limit import rate_limiter
from app.db import SessionLocal, PredictionLog, init_db  # ADD THIS
import json  # ADD THIS

init_db()  # Ensure the DB and table are created at startup

app = FastAPI()

@app.post("/predict")
async def predict_bank_churn(
    customer: ChurnInput,
    request: Request,
    authorization: str = Header(...)):
    
    await rate_limiter(request)
    token = authorization.split(" ")[1]
    user_id = verify_token(token)
    pred = predict_churn(customer.features)
    status = "CHURN" if pred == 1 else "RETAIN"

    # === SAVE LOG TO DATABASE ===
    db = SessionLocal()
    try:
        log = PredictionLog(
            user_id=user_id,
            features=json.dumps(customer.features),
            prediction=status,
        )
        db.add(log)
        db.commit()
    finally:
        db.close()
    # === END DB LOGGING ===

    return {"customer_status": status, "user": user_id}
