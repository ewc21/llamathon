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

  // *** ADD THESE LINES ***
  const [isLoading, setIsLoading] = useState(false); // State for loading indicator
  const [error, setError] = useState(null); // State for error messages
  // *** END OF ADDED LINES ***

  // Function to handle submitting a log entry
  const handleLogSubmit = async (mealType, inputText) => {
    console.log(`Submitting to backend for ${mealType}: ${inputText}`);
    setIsLoading(true); // Set loading true
    setError(null); // Clear previous errors

    try {
      const response = await fetch("/api/chat", {
        // Use your actual backend endpoint
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // TODO: Add Authorization header with token when auth is implemented
          // 'Authorization': `Bearer ${your_auth_token}`
        },
        body: JSON.stringify({
          prompt: inputText,
          meal_type: mealType, // Send the meal type
          // TODO: Add user_id when auth is implemented
        }),
      });

      if (!response.ok) {
        // Try to get error details from response body
        let errorDetail = `API Error: ${response.status} ${response.statusText}`;
        try {
          const errorData = await response.json();
          errorDetail = errorData.detail || errorDetail;
        } catch (e) {
          /* Ignore if response body isn't JSON */
        }
        throw new Error(errorDetail);
      }

      const data = await response.json();
      console.log("API Response:", data);

      // Process the response which contains the items saved in the DB
      const newItems = data.logged_items || []; // Use the key returned by backend

      // Update the correct meal state
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
        default:
          console.error("Unknown meal type:", mealType);
      }
    } catch (err) {
      console.error("Failed to log meal:", err);
      setError(err.message || "Failed to connect to the server."); // Set error state
      // Optionally display this error to the user in the UI
    } finally {
      setIsLoading(false); // Set loading false regardless of success/failure
    }
  };

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
        // Ensure these keys match the column names returned from backend
        acc.calories += item?.calories || 0;
        acc.protein += item?.protein || 0;
        acc.carbohydrates += item?.carbohydrates || 0;
        acc.fat += item?.fat || 0;
        acc.fiber += item?.fiber || 0;
        acc.sodium += item?.sodium || 0;
        // Add other micros here if you want them in the DailyOverview totals
        acc.calcium += item?.calcium || 0;
        acc.iron += item?.iron || 0;
        acc.potassium += item?.potassium || 0;
        // ... etc.
        return acc;
      },
      {
        calories: 0,
        protein: 0,
        carbohydrates: 0,
        fat: 0,
        fiber: 0,
        sodium: 0,
        calcium: 0,
        iron: 0,
        potassium: 0 /* Init other micros */,
      }
    );

    setDailyTotals(totals);
  }, [breakfastItems, lunchItems, dinnerItems, snackItems]);

  return (
    <div className="dashboard-container">
      {/* ... (keep header) ... */}
      <header className="dashboard-header">
        <img src={LlamaLogo} alt="Llama Logo" className="dashboard-logo" />
        {/* Add User Profile/Logout later */}
      </header>

      {/* Display Loading/Error State */}
      {isLoading && (
        <div className="loading-indicator">Logging your meal...</div>
      )}
      {error && <div className="error-message">Error: {error}</div>}

      <div className="dashboard-content">
        {/* Left Panel: Meal Sections */}
        <div className="meal-sections-panel">
          {/* Pass handleLogSubmit to each MealSection */}
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
          <DailyOverview dailyTotals={dailyTotals} />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
