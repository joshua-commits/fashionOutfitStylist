from pathlib import Path
import numpy as np
import json
from tqdm import tqdm
from backend.models import ClothingItem
from backend.database import SessionLocal
from app.embeddings.clip_model import embed_image  # your CLIP helper

# Create DB session
db = SessionLocal()

# Load all items from database
items = db.query(ClothingItem).all()

# Output folders
output_dir = Path("static/embeddings")
output_dir.mkdir(parents=True, exist_ok=True)

embeddings = []
metadata = []

# Loop through all images
for item in tqdm(items, desc="Embedding images"):
    try:
        emb = embed_image(item.image_path)  # returns a numpy array
        embeddings.append(emb)
        metadata.append({
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "image_path": item.image_path
        })
    except Exception as e:
        print(f"Error embedding {item.image_path}: {e}")

# Save embeddings & metadata
embeddings = np.array(embeddings).astype("float32")
np.save(output_dir / "image_vectors.npy", embeddings)

with open(output_dir / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Completed embeddings for {len(embeddings)} images")