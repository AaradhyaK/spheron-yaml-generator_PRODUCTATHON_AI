from pydantic import BaseModel
from typing import Optional

class YAMLResponse(BaseModel):
    yaml: str
