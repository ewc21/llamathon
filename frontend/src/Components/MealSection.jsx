import React, { useState } from "react";
import FoodItem from "./FoodItem";
import "../Styles/MealSection.css";

const MealSection = ({ title, mealType, items, onLogSubmit }) => {
  const [isInputVisible, setIsInputVisible] = useState(false);
  const [inputText, setInputText] = useState("");
  const [chatMessages, setChatMessages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const result = await onLogSubmit(mealType, inputText);

    if (result?.success && result.messages?.length) {
      setChatMessages((prev) => [...prev, ...result.messages]);
    }

    setInputText("");
    setIsInputVisible(false);
  };

  const handleAddClick = () => {
    setIsInputVisible(true);
  };

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  return (
    <div className="meal-section">
      <div className="meal-header">
        <h3>{title}</h3>
        {!isInputVisible && (
          <button onClick={handleAddClick} className="add-button">
            +
          </button>
        )}
      </div>

      <div className="food-list">
        {items.map((item, index) => (
          <FoodItem key={item._id || `${mealType}-${index}`} foodData={item} />
        ))}
        {items.length === 0 && !isInputVisible && (
          <p className="empty-meal-text">No items logged yet.</p>
        )}
      </div>

      {/* Chat-style feedback */}
      <div className="meal-chat">
        {chatMessages.map((msg, idx) => (
          <div key={idx} className="chat-bubble">
            {msg}
          </div>
        ))}
      </div>

      {isInputVisible && (
        <form onSubmit={handleSubmit} className="log-form">
          <input
            type="text"
            placeholder={`Log ${title.toLowerCase()}... (e.g., "2 eggs and toast")`}
            value={inputText}
            onChange={handleInputChange}
            className="log-input"
            autoFocus
          />
          <button type="submit" className="log-submit-button">
            Log
          </button>
          <button
            type="button"
            onClick={() => setIsInputVisible(false)}
            className="log-cancel-button"
          >
            Cancel
          </button>
        </form>
      )}
    </div>
  );
};

export default MealSection;
