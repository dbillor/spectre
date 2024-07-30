from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
from data  import models, schemas, crud
from data.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/nodes/", response_model=schemas.Node)
def create_node(node: schemas.NodeCreate, db: Session = Depends(get_db)):
    return crud.create_node(db=db, node=node)

@app.get("/nodes/", response_model=List[schemas.Node])
def read_nodes(filters: Optional[Dict[str, str]] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_nodes(db=db, filters=filters, skip=skip, limit=limit)

@app.post("/links/", response_model=schemas.Link)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    return crud.create_link(db=db, link=link)

@app.get("/links/", response_model=List[schemas.Link])
def read_links(node_ids: Optional[List[int]] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_links(db=db, node_ids=node_ids, skip=skip, limit=limit)

@app.get("/data/", response_model=Dict[str, List[schemas.Node]])
def read_all_data(filters: Optional[Dict[str, str]] = None, node_ids: Optional[List[int]] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_data(db=db, filters=filters, node_ids=node_ids, skip=skip, limit=limit)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
