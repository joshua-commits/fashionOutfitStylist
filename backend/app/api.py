from os import name
import stat
from unicodedata import category
from fastapi import FastAPI, HTTPException, UploadFile, File, status, Form, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import aiofiles
from pathlib import Path

# database
from .. import models, database

# creates the database
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Fashion Outfit Stylist - Backend (MVP)")

# Allow requests from your React dev server (Vite default: port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload", status_code=201)
async def upload_image(
    file: UploadFile = File(...),
    name: str = Form(...),
    category: str = Form(...),
    color: str = Form(None),
    style: str = Form(None),
    user_id: int | None = Form(None),
    db: Session = Depends(get_db),
):


    """
    Upload a clothing image and save metadata to the database.
    """

    # save uploaded file
    file_path = UPLOAD_DIR / file.filename
    try: # added exception handling
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

     # Create new clothing item entry in the database
    try:
        new_item = models.ClothingItem(
            name=name,
            category=category,
            color=color,
            style=style,
            image_path=str(file_path),
            owner_id=user_id
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    # Future placeholder for ML preprocessing (e.g., embeddings)
    # preprocess_image(file_path)

    return {
        "id": new_item.id,
        "name": new_item.name,
        "filename": file.filename,
        "image_path": str(file_path),
        "message": "Upload successful!"
    }