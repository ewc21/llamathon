import React, { useState, useEffect } from "react";
import MealSection from "../Components/MealSection";
import DailyOverview from "../Components/DailyOverview";
import LlamaLogo from "../assets/LlamaLogo.png";
import "../Styles/DashboardPage.css"; // Keep existing styles, may need adjustments

const DashboardPage = () => {
  // State for each meal's items
  const [breakfastItems, setBreakfastItems] = useState([]);
  const [lunchItems, setLunchItems] = useState([]);
  const [dinnerItems, setDinnerItems] = useState([]);
  const [snackItems, setSnackItems] = useState([]);

  // State for daily totals
  const [dailyTotals, setDailyTotals] = useState({
    calories: 0,
    protein: 0,
    carbohydrates: 0,
    fat: 0,
    fiber: 0,
    sodium: 0, // Add more micros
  });

  const handleLogSubmit = async (mealType, inputText) => {
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: inputText }),
      });

      if (!response.ok) {
        console.error("API Error:", response.statusText);
        return { success: false };
      }

      const data = await response.json();
      const parsed = JSON.parse(data.response);

      const analysis = parsed.health_analysis || {};
      const newItems = (parsed.meal_items || []).map((item, idx) => ({
        ...item,
        health_analysis: analysis,
        _id: `${Date.now()}-${idx}`, // ensure uniqueness
      }));

      switch (mealType) {
        case "breakfast":
          setBreakfastItems((prev) => [...prev, ...newItems]);
          break;
        case "lunch":
          setLunchItems((prev) => [...prev, ...newItems]);
          break;
        case "dinner":
          setDinnerItems((prev) => [...prev, ...newItems]);
          break;
        case "snacks":
          setSnackItems((prev) => [...prev, ...newItems]);
          break;
      }

      return { success: true, messages: [] };
    } catch (err) {
      console.error("Request failed:", err);
      return { success: false };
    }
  };

  // Calculate totals whenever any meal items change
  useEffect(() => {
    const allItems = [
      ...breakfastItems,
      ...lunchItems,
      ...dinnerItems,
      ...snackItems,
    ];
    const totals = allItems.reduce(
      (acc, item) => {
        // Sum up nutrients, handling potential missing values
        acc.calories += item?.calories || item?.macros?.calories || 0;
        acc.protein += item?.protein || item?.macros?.protein || 0;
        acc.carbohydrates +=
          item?.carbohydrates || item?.macros?.carbohydrates || 0;
        acc.fat += item?.fat || item?.macros?.fat || 0;
        acc.fiber += item?.fiber || item?.micros?.fiber || 0;
        acc.sodium += item?.sodium || item?.micros?.sodium || 0;
        // Add other micros here
        return acc;
      },
      {
        calories: 0,
        protein: 0,
        carbohydrates: 0,
        fat: 0,
        fiber: 0,
        sodium: 0 /* Init other micros */,
      }
    );

    setDailyTotals(totals);
  }, [breakfastItems, lunchItems, dinnerItems, snackItems]);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <img src={LlamaLogo} alt="Llama Logo" className="dashboard-logo" />
        {/* Add User Profile/Logout later */}
      </header>

      <div className="dashboard-content">
        {/* Left Panel: Meal Sections */}
        <div className="meal-sections-panel">
          {" "}
          {/* New wrapper div */}
          <MealSection
            title="Breakfast"
            mealType="breakfast"
            items={breakfastItems}
            onLogSubmit={handleLogSubmit}
          />
          <MealSection
            title="Lunch"
            mealType="lunch"
            items={lunchItems}
            onLogSubmit={handleLogSubmit}
          />
          <MealSection
            title="Dinner"
            mealType="dinner"
            items={dinnerItems}
            onLogSubmit={handleLogSubmit}
          />
          <MealSection
            title="Snacks"
            mealType="snacks"
            items={snackItems}
            onLogSubmit={handleLogSubmit}
          />
        </div>

        {/* Right Panel: Daily Overview */}
        <div className="stats-panel">
          {" "}
          {/* Re-using existing class */}
          <DailyOverview dailyTotals={dailyTotals} />
          {/* We removed the individual StatsCards */}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
