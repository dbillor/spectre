from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import relationship
from .database import Base

class Node(Base):
    __tablename__ = "nodes"

    id = Column(String, primary_key=True, index=True)
    color = Column(String)
    size = Column(Float)
    type = Column(String)
    dc = Column(String)
    set = Column(String)
    status = Column(String)
    vendor = Column(String)
    cloudtype = Column(String)
    devicetype = Column(String)
    continent = Column(String)
    country = Column(String)
    region = Column(String)


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    target = Column(String, index=True)
    value = Column(Float)
    color = Column(String)
    start_int = Column(String)
    end_int = Column(String)

    source_node = relationship("Node", foreign_keys=[source], back_populates="outgoing_links")
    target_node = relationship("Node", foreign_keys=[target], back_populates="incoming_links")


Node.outgoing_links = relationship("Link", foreign_keys=[Link.source], back_populates="source_node")
Node.incoming_links = relationship("Link", foreign_keys=[Link.target], back_populates="target_node")









