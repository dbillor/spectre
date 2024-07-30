from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import  models, schemas
from typing import List, Dict, Optional


def get_nodes(db: Session, filters: Dict[str, str] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Node)
    if filters:
        for key, value in filters.items():
            if hasattr(models.Node, key):
                query = query.filter(getattr(models.Node, key) == value)
    return query.offset(skip).limit(limit).all()

def get_links(db: Session, node_ids: List[str] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Link)
    if node_ids:
       query = query.filter(or_(models.Link.source.in_(node_ids), models.Link.target.in_(node_ids))) 
    return query.offset(skip).limit(limit).all()

def get_all_data(db: Session, filters: Optional[Dict[str, str]] = None, node_ids:
    Optional[List[int]] = None, skip: int = 0, limit: int = 100):
    nodes = get_nodes(db, filters, skip, limit)
    links = get_links(db, node_ids, skip, limit)
    return {"nodes" : nodes, "links" : links}

def get_nodes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Node).offset(skip).limit(limit).all()

def create_node(db: Session, node: schemas.NodeCreate):
    db_node = models.Node(**node.dict())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node     

def create_link(db: Session, link: schemas.LinkCreate):
    db_link = models.Link(**link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

