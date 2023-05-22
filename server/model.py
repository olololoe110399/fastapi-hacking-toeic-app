from typing import Optional

from pydantic import BaseModel


class ReadingSchema(BaseModel):
    question: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "question": """Managers need to know what motivates their employees to ___ them committed to their organization.
                (A) keep
                (B) feature
                (C) enable
                (D) become""",
            }
        }
