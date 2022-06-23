from typing import List
from pydantic import BaseModel
from typing import Optional

class Diary(BaseModel):
    content: Optional[str] = None
    photo: Optional[str] = None
    visible: Optional[int] = None