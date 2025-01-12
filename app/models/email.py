from pydantic import BaseModel
from datetime import datetime

class EmailData(BaseModel):
    subject: str
    sender: str
    received_at: datetime
    content: str
    message_id: str