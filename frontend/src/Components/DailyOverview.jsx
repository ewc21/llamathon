import React from 'react';
import '../Styles/DailyOverview.css';

// Example structure for totals - this will come from DashboardPage state
const mockTotals = {
  calories: 0,
  protein: 0,
  carbohydrates: 0,
  fat: 0,
  fiber: 0,
  sodium: 0,
  // ... other aggregated micros
};

const DailyOverview = ({ dailyTotals = mockTotals }) => {
  return (
    <div className="daily-overview">
      <h2>Daily Totals</h2>
      <div className="totals-grid">
        <div className="total-item">
            <span className="total-label">Calories</span>
            <span className="total-value">{dailyTotals.calories || 0} kcal</span>
        </div>
         <div className="total-item">
            <span className="total-label">Protein</span>
            <span className="total-value">{dailyTotals.protein || 0} g</span>
        </div>
         <div className="total-item">
            <span className="total-label">Carbs</span>
            <span className="total-value">{dailyTotals.carbohydrates || 0} g</span>
        </div>
         <div className="total-item">
            <span className="total-label">Fat</span>
            <span className="total-value">{dailyTotals.fat || 0} g</span>
        </div>
         <div className="total-item">
            <span className="total-label">Fiber</span>
            <span className="total-value">{dailyTotals.fiber || 0} g</span>
        </div>
         <div className="total-item">
            <span className="total-label">Sodium</span>
            <span className="total-value">{dailyTotals.sodium || 0} mg</span>
        </div>
        {/* Add more rows for other important micros */}
      </div>
       {/* Optionally add goal comparisons later */}
    </div>
  );
};

export default DailyOverview;