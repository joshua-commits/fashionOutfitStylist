import React, { useState } from "react";
import { uploadImage } from "../api";

const ImageUploader: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first.");
    setLoading(true);
    try {
      const data = await uploadImage(file);
      setPreviewUrl(`http://127.0.0.1:8000${data.url}`);
    } catch (err) {
      console.error(err);
      alert("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4 p-6 border rounded-2xl w-full max-w-md mx-auto">
      <h2 className="text-xl font-semibold">Upload Image</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
      {previewUrl && (
        <div className="mt-4">
          <img
            src={previewUrl}
            alt="Uploaded preview"
            className="rounded-lg max-h-64"
          />
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
