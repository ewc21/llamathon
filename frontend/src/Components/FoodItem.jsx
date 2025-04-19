import React, { useState } from 'react';
import '../Styles/FoodItem.css';

// Mock data structure until backend is connected
const mockFoodData = {
  name: 'Placeholder Food',
  calories: 100,
  protein: 10,
  carbohydrates: 15,
  fat: 5,
  // Add mock micros later if needed for dropdown testing
  fiber: 2,
  iron: 1,
  calcium: 50,
  // ... other micros
};


const FoodItem = ({ foodData = mockFoodData }) => { // Use mock data as default for now
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  // Helper to safely access potentially missing data
  const getNutrient = (key, unit = 'g') => {
      const value = foodData?.macros?.[key] ?? foodData?.[key] ?? 0; // Check macros first, then top level
      return `${value}${unit}`;
  }
  const getMicro = (key, unit = 'mg') => {
      const value = foodData?.micros?.[key] ?? 0;
      return `${value}${unit}`;
  }


  return (
    <div className="food-item">
      <div className="food-item-summary" onClick={toggleExpand}>
        <span className="food-name">{foodData?.name || 'Unknown Item'}</span>
        <div className="food-macros-summary">
          <span>{getNutrient('calories', 'kcal')}</span>
          <span>P: {getNutrient('protein')}</span>
          <span>C: {getNutrient('carbohydrates')}</span>
          <span>F: {getNutrient('fat')}</span>
        </div>
        <button className="expand-button">{isExpanded ? '▲' : '▼'}</button>
      </div>

      {/* Expanded view with details */}
      {isExpanded && (
        <div className="food-item-details">
          <h4>Full Nutrition (per {foodData?.quantity || 'serving'}):</h4>
          {/* Display all macros and micros */}
          <p><strong>Calories:</strong> {getNutrient('calories', 'kcal')}</p>
          <p><strong>Protein:</strong> {getNutrient('protein')}</p>
          <p><strong>Carbohydrates:</strong> {getNutrient('carbohydrates')}</p>
          <p><strong>Fat:</strong> {getNutrient('fat')}</p>
          <p><strong>Fiber:</strong> {getMicro('fiber', 'g')}</p>
          <p><strong>Sodium:</strong> {getMicro('sodium', 'mg')}</p>
          <p><strong>Sugar:</strong> {getMicro('sugar', 'g')}</p> {/* Assuming sugar might be in micros */}
          <p><strong>Iron:</strong> {getMicro('iron', 'mg')}</p>
          <p><strong>Calcium:</strong> {getMicro('calcium', 'mg')}</p>
          <p><strong>Potassium:</strong> {getMicro('potassium', 'mg')}</p>
           {/* Add other micros as available from backend */}
           <p><strong>Vitamin A:</strong> {getMicro('vitamin A', '%')}</p>
           <p><strong>Vitamin C:</strong> {getMicro('vitamin C', '%')}</p>
           {/* ... etc */}
        </div>
      )}
    </div>
  );
};

export default FoodItem;