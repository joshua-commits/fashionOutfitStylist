from PIL import Image, ImageOps
import imagehash
from pathlib import Path

TARGET_SIZE = (512, 512)

def preprocess_image(input_path: Path, output_dir: Path) -> dict:
    """Process uploaded image: fix EXIF, resize, pad, hash, and save."""


    image = Image.open(input_path)
    image = ImageOps.exif_transpose(image)

    image.thumbnail(TARGET_SIZE, Image.Resampling.LANCZOS)
    new_img = Image.new("RGB", TARGET_SIZE, (255, 255, 255)) 
    offset = ((TARGET_SIZE[0] - image.width) // 2, (TARGET_SIZE[1] - image.height) // 2)
    new_img.paste(image, offset)

    img_hash = str(imagehash.average_hash(new_img))


    output_dir.mkdir(parents=True, exist_ok=True)
    processed_path = output_dir / input_path.name
    new_img.save(processed_path, format="JPEG", quality=95)

    return {
        "hash": img_hash,
        "processed_path": str(processed_path),
        "original_size": image.size,
        "processed_size": new_img.size,
    }