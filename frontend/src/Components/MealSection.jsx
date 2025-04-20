import React, { useState } from 'react';
import FoodItem from './FoodItem'; // We'll create this next
import '../Styles/MealSection.css';

const MealSection = ({ title, mealType, items, onLogSubmit }) => {
  const [isInputVisible, setIsInputVisible] = useState(false);
  const [inputText, setInputText] = useState('');

  const handleAddClick = () => {
    setIsInputVisible(true);
  };

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent page reload on form submit
    if (!inputText.trim()) return; // Don't submit empty text

    console.log(`Submitting for ${mealType}: ${inputText}`); // Placeholder
    // In the future, call the actual API function passed via onLogSubmit
    onLogSubmit(mealType, inputText);
    setInputText('');
    setIsInputVisible(false);
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

      {/* List of logged food items */}
      <div className="food-list">
        {items.map((item, index) => (
          <FoodItem key={`${mealType}-${index}`} foodData={item} />
        ))}
        {items.length === 0 && !isInputVisible && (
           <p className="empty-meal-text">No items logged yet.</p>
        )}
      </div>

      {/* Input area that appears when '+' is clicked */}
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
           <button type="button" onClick={() => setIsInputVisible(false)} className="log-cancel-button">
            Cancel
          </button>
        </form>
      )}
    </div>
  );
};

export default MealSection;