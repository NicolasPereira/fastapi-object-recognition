import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form

app = FastAPI()


@app.get("/")
def read_root():
  return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}

@app.post("/files/")
async def create_file(file: UploadFile = File(...)):
  with open(f'{file.filename}', "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
  
  return {"file_name": file.filename}