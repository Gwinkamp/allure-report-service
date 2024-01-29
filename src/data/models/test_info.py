from typing import List, Optional

from pydantic import BaseModel


class TestInfo(BaseModel):
    """Данные автотеста"""
    short_name: str
    full_name: Optional[str]
    story: Optional[str]
    feature: Optional[str]
    epic: Optional[str]
    tags: List[str]
    severity: Optional[str]
