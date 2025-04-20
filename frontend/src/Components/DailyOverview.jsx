import React, { useEffect, useState } from "react";
import "../Styles/DailyOverview.css";

const USER_ID = 123;
const API_BASE_URL = "http://localhost:8000";

const DailyOverview = () => {
  const [totals, setTotals] = useState({
    calories: 0,
    protein: 0,
    carbohydrates: 0,
    fat: 0,
    fiber: 0,
    sodium: 0,
  });

  const getTodayDate = () => {
    const today = new Date();
    return today.toISOString().split("T")[0]; // YYYY-MM-DD
  };

  useEffect(() => {
    const fetchDailyTotals = async () => {
      try {
        const date = getTodayDate();
        const response = await fetch(
          `${API_BASE_URL}/meals/${USER_ID}/${date}`
        );
        const data = await response.json();
        const items = data.meal_items || [];

        const aggregated = items.reduce(
          (acc, item) => {
            acc.calories += item.calories || 0;
            acc.protein += item.protein || 0;
            acc.carbohydrates += item.carbs || 0;
            acc.fat += item.fat || 0;
            acc.fiber += item.fiber || 0;
            acc.sodium += item.sodium || 0;
            return acc;
          },
          {
            calories: 0,
            protein: 0,
            carbohydrates: 0,
            fat: 0,
            fiber: 0,
            sodium: 0,
          }
        );

        setTotals(aggregated);
      } catch (error) {
        console.error("Error fetching daily totals:", error);
      }
    };

    fetchDailyTotals();
  }, []);

  return (
    <div className="daily-overview">
      <h2>Daily Totals</h2>
      <div className="totals-grid">
        <div className="total-item">
          <span className="total-label">Calories</span>
          <span className="total-value">{totals.calories} kcal</span>
        </div>
        <div className="total-item">
          <span className="total-label">Protein</span>
          <span className="total-value">{totals.protein} g</span>
        </div>
        <div className="total-item">
          <span className="total-label">Carbs</span>
          <span className="total-value">{totals.carbohydrates} g</span>
        </div>
        <div className="total-item">
          <span className="total-label">Fat</span>
          <span className="total-value">{totals.fat} g</span>
        </div>
        <div className="total-item">
          <span className="total-label">Fiber</span>
          <span className="total-value">{totals.fiber} g</span>
        </div>
        <div className="total-item">
          <span className="total-label">Sodium</span>
          <span className="total-value">{totals.sodium} mg</span>
        </div>
      </div>
    </div>
  );
};

export default DailyOverview;
