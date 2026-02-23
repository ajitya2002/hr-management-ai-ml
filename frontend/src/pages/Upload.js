
import React from "react";
import axios from "axios";

function Upload() {
  const handleUpload = async (e) => {
    const formData = new FormData();
    formData.append("file", e.target.files[0]);

    await axios.post("http://localhost:8000/upload", formData);
    alert("HR Policy Uploaded Successfully");
  };

  return (
    <div>
      <h2>Upload HR Policy PDF</h2>
      <input type="file" onChange={handleUpload} />
    </div>
  );
}

export default Upload;
