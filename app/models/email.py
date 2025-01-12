from datetime import datetime

from pydantic import BaseModel


class EmailData(BaseModel):
    subject: str
    sender: str
    received_at: datetime
    content: str
    message_id: str