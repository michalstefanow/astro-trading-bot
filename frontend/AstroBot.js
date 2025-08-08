import React, { useState } from "react";

export default function AstroBot() {
    const [chat, setChat] = useState([]);
    const [input, setInput] = useState("");

    const sendMessage = () => {
        const newChat = [...chat, { sender: "You", text: input }];
        newChat.push({ sender: "AstroBot", text: "Got it! I'll log this for future learning." });
        setChat(newChat);
        setInput("");
    };

    return (
        <div className="mt-6 p-4 bg-gray-900 rounded-xl">
            <h2 className="text-lg font-semibold mb-2">🧠 AstroBot</h2>
            <div className="max-h-48 overflow-y-auto mb-2">
                {chat.map((msg, i) => (
                    <div key={i}><strong>{msg.sender}:</strong> {msg.text}</div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="w-full p-2 text-black"
                placeholder="Type a trade update or question..."
            />
            <button onClick={sendMessage} className="mt-2 px-4 py-2 bg-blue-600 rounded">Send</button>
        </div>
    );
}