// src/Components/ChatWindow.jsx
import React from "react";
import "../Styles/ChatWindow.css";

const ChatWindow = () => {
  return (
    <div className="chat-window">
      <div className="chat-messages">
        <p>Welcome to LlamaNutrition!</p>
        <p>Start logging your meals below.</p>
      </div>
      <div className="chat-bar">
        <input
          className="chat-input"
          type="text"
          placeholder="Enter Nutrition Data"
        />
        <button className="chat-submit" type="button">
          Enter
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
