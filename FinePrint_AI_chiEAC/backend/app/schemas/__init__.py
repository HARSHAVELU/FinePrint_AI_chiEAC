from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
class Row(BaseModel):
    model_config = ConfigDict(extra='ignore')
    doc_id: str = Field(min_length=1, max_length=200)
    section_id: str = Field(min_length=1, max_length=100)
    heading: str = Field(default='', max_length=1000)
    text: str = Field(min_length=1, max_length=50000)
    page: int | None = Field(default=None, ge=1)
    source_file: str = ''
class Item(BaseModel):
    item_type: Literal['deadline','requirement','fee','obligation','missing','term']
    value: str
    section_id: str
    quote: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    explanation: str = ''
    inference: str = ''
    badge: Literal['High','Medium','Low'] = 'Low'
    verified: bool = False
    match: str = ''
class CandidateList(BaseModel):
    items: list[Item]
class SessionRequest(BaseModel):
    session_id: str = Field(min_length=20, max_length=200)
class AskRequest(SessionRequest):
    question: str = Field(min_length=1, max_length=1000)
class SearchRequest(AskRequest):
    pass
