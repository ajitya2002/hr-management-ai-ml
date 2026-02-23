
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Upload from "./pages/Upload";
import Chat from "./pages/Chat";

function App() {
  return (
    <Router>
      <div style={{ display: "flex" }}>
        <div style={{ width: "200px", padding: "20px", background: "#1e293b", color: "white" }}>
          <h3>HR LLM</h3>
          <Link to="/" style={{ color: "white", display: "block", margin: "10px 0" }}>Upload</Link>
          <Link to="/chat" style={{ color: "white", display: "block" }}>Chat</Link>
        </div>
        <div style={{ flex: 1, padding: "20px" }}>
          <Routes>
            <Route path="/" element={<Upload />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
