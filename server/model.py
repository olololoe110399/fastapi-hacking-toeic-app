from typing import Optional

from pydantic import BaseModel

class ReadingSchema(BaseModel):
    question: Optional[str]
    options: Optional[list]

    class Config:
        schema_extra = {
            "example": {
                "question": "Managers need to know what motivates their employees to ___ them committed to their organization",
                "options": ['across','into','between','despite']
            }
        }