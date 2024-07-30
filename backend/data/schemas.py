from pydantic import BaseModel
from typing import Optional

class NodeBase(BaseModel):
    id: str
    color: str
    size: float
    type: str
    dc: str
    set: str
    status: str
    vendor: str
    cloudtype: str
    region: str
    deviceypte: str

class NodeCreate(NodeBase):
    pass

class Node(NodeBase):
    class Config:
        orm_mode = True

class LinkBase(BaseModel):
    source: str
    target: str
    value: float
    color: str
    start_int: str
    end_int: str

class LinkCreate(LinkBase):
    pass

class Link(LinkBase):
    pass

class Link(LinkBase):
    id: int

class Config:
    orm_mode = True
