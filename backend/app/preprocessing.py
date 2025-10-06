from PIL import Image, ImageOps
import imagehash
from pathlib import Path

TARGET_SIZE = (512, 512)

def preprocess_image(input_path: Path, output_dir: Path) -> dict:
    """Process uploaded image: fix EXIF, resize, pad, hash, and save."""

    # 1️⃣ Load image & fix EXIF orientation
    image = Image.open(input_path)
    image = ImageOps.exif_transpose(image)

    # 2️⃣ Preserve aspect ratio (pad to target)
    image.thumbnail(TARGET_SIZE, Image.Resampling.LANCZOS)
    new_img = Image.new("RGB", TARGET_SIZE, (255, 255, 255))  # white background
    offset = ((TARGET_SIZE[0] - image.width) // 2, (TARGET_SIZE[1] - image.height) // 2)
    new_img.paste(image, offset)

    # 3️⃣ Hash (for duplicate detection)
    img_hash = str(imagehash.average_hash(new_img))

    # 4️⃣ Save processed image
    output_dir.mkdir(parents=True, exist_ok=True)
    processed_path = output_dir / input_path.name
    new_img.save(processed_path, format="JPEG", quality=95)

    # 5️⃣ Return metadata
    return {
        "hash": img_hash,
        "processed_path": str(processed_path),
        "original_size": image.size,
        "processed_size": new_img.size,
    }