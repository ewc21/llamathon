import React, { useState } from "react";
import "../Styles/FoodItem.css";

const mockFoodData = {
  name: "Placeholder Food",
  calories: 100,
  protein: 10,
  carbohydrates: 15,
  fat: 5,
  fiber: 2,
  iron: 1,
  calcium: 50,
};

const FoodItem = ({ foodData = mockFoodData }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const getNutrient = (key, unit = "g") => {
    const value = foodData?.macros?.[key] ?? foodData?.[key] ?? 0;
    return `${value}${unit}`;
  };

  const getMicro = (key, unit = "mg") => {
    const value = foodData?.micros?.[key] ?? 0;
    return `${value}${unit}`;
  };

  return (
    <div className="food-item">
      <div className="food-item-summary" onClick={toggleExpand}>
        <span className="food-name">{foodData?.name || "Unknown Item"}</span>
        <div className="food-macros-summary">
          <span>{getNutrient("calories", "kcal")}</span>
          <span>P: {getNutrient("protein")}</span>
          <span>C: {getNutrient("carbohydrates")}</span>
          <span>F: {getNutrient("fat")}</span>
        </div>
        <button className="expand-button">{isExpanded ? "▲" : "▼"}</button>
      </div>

      {isExpanded && (
        <div className="food-item-details">
          <h4>Full Nutrition (per {foodData?.quantity || "serving"}):</h4>
          <p>
            <strong>Calories:</strong> {getNutrient("calories", "kcal")}
          </p>
          <p>
            <strong>Protein:</strong> {getNutrient("protein")}
          </p>
          <p>
            <strong>Carbohydrates:</strong> {getNutrient("carbohydrates")}
          </p>
          <p>
            <strong>Fat:</strong> {getNutrient("fat")}
          </p>
          <p>
            <strong>Fiber:</strong> {getMicro("fiber", "g")}
          </p>
          <p>
            <strong>Sodium:</strong> {getMicro("sodium", "mg")}
          </p>
          <p>
            <strong>Sugar:</strong> {getMicro("sugar", "g")}
          </p>
          <p>
            <strong>Iron:</strong> {getMicro("iron", "mg")}
          </p>
          <p>
            <strong>Calcium:</strong> {getMicro("calcium", "mg")}
          </p>
          <p>
            <strong>Potassium:</strong> {getMicro("potassium", "mg")}
          </p>
          <p>
            <strong>Vitamin A:</strong> {getMicro("vitamin A", "%")}
          </p>
          <p>
            <strong>Vitamin C:</strong> {getMicro("vitamin C", "%")}
          </p>

          {foodData.health_analysis && (
            <div className="health-analysis">
              <br />
              <p>
                <strong>Summary:</strong> {foodData.health_analysis.summary}
              </p>
              <p>
                <strong>Contribution:</strong>{" "}
                {foodData.health_analysis.new_meal_contribution}
              </p>
              <p>
                <strong>Verdict:</strong> {foodData.health_analysis.verdict}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FoodItem;
