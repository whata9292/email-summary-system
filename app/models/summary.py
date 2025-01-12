from datetime import datetime

from pydantic import BaseModel


class Summary(BaseModel):
    email_id: str
    content: str
    generated_at: datetime