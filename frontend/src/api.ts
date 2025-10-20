export async function uploadImage(
  file: File,
  name: string,
  category: string,
  color?: string,
  style?: string,
  userId?: number) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);
  formData.append("category", category);
  
  if (color) formData.append("color", color);
  if (style) formData.append("style", style);
  if (userId !== undefined) formData.append("user_id", String(userId));
  
  const res = await fetch("http://127.0.0.1:8000/upload", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    console.error("Upload error:", err);
    throw new Error(`Upload failed: ${res.status}`);
  }
  return res.json();
}