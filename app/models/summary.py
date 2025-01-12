from pydantic import BaseModel
from datetime import datetime

class Summary(BaseModel):
    email_id: str
    content: str
    generated_at: datetime