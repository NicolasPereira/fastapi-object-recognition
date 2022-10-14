import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form
from detect_image import detect

app = FastAPI()


@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.post("/files/")
async def create_file(file: UploadFile = File(...)):
  with open(f'{file.filename}', "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
  
  dados = detect.detect(file.filename)
  return dados