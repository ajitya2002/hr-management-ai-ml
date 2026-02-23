
import React, { useState } from "react";
import axios from "axios";

function Chat() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    const res = await axios.post("http://localhost:8000/ask?query=" + message);
    setChat([...chat, { q: message, a: res.data.answer }]);
    setMessage("");
  };

  return (
    <div>
      <h2>HR AI Chat Assistant</h2>
      {chat.map((c, i) => (
        <div key={i}>
          <p><b>You:</b> {c.q}</p>
          <p><b>AI:</b> {c.a}</p>
        </div>
      ))}
      <input value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chat;
