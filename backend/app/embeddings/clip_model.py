from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

image = Image.open("static/processed/top1.jpg")
inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    embeddings = model.get_image_features(**inputs)