from pydantic import BaseModel, conlist

class ChurnInput(BaseModel):
    features: conlist(float, min_length=10, max_length=10)
