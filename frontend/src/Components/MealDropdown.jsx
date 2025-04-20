import React, { useState } from "react";
import "../Styles/MealDropdown.css";

const USER_ID = 123; // Replace with dynamic value if needed
const API_BASE_URL = "http://localhost:8000"; // Change to your actual backend URL

const MealDropdown = () => {
  const [selectedDate, setSelectedDate] = useState("");
  const [meals, setMeals] = useState([]);
  const [open, setOpen] = useState(false);

  const fetchMeals = async (date) => {
    try {
      const response = await fetch(`${API_BASE_URL}/meals/${USER_ID}/${date}`);
      const data = await response.json();
      setMeals(data.meal_items || []);
      setOpen(true);
    } catch (error) {
      console.error("Failed to fetch meal data:", error);
      setMeals([]);
      setOpen(true);
    }
  };

  const calculateTotal = (key) =>
    meals.reduce((sum, item) => sum + (item[key] || 0), 0);

  return (
    <div className="meal-dropdown-container">
      <label htmlFor="dateSelect">Select a date:</label>
      <input
        id="dateSelect"
        type="date"
        value={selectedDate}
        onChange={(e) => {
          const date = e.target.value;
          setSelectedDate(date);
          fetchMeals(date);
        }}
        className="custom-select"
      />

      {open && (
        <div className="modal-overlay" onClick={() => setOpen(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{selectedDate} — Meals</h2>
            <table className="meal-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Calories</th>
                  <th>Protein (g)</th>
                  <th>Carbs (g)</th>
                  <th>Fat (g)</th>
                  <th>Meal Type</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {meals.length === 0 ? (
                  <tr>
                    <td colSpan="7" style={{ textAlign: "center" }}>
                      No meals logged.
                    </td>
                  </tr>
                ) : (
                  meals.map((item) => (
                    <tr key={item.id}>
                      <td>{item.name}</td>
                      <td>{item.calories}</td>
                      <td>{item.protein}</td>
                      <td>{item.carbs}</td>
                      <td>{item.fat}</td>
                      <td>{item.meal_type}</td>
                      <td>
                        {new Date(item.timestamp).toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </td>
                    </tr>
                  ))
                )}
                {meals.length > 0 && (
                  <tr className="total-row">
                    <td>
                      <strong>Total</strong>
                    </td>
                    <td>{calculateTotal("calories")}</td>
                    <td>{calculateTotal("protein")}</td>
                    <td>{calculateTotal("carbs")}</td>
                    <td>{calculateTotal("fat")}</td>
                    <td colSpan="2"></td>
                  </tr>
                )}
              </tbody>
            </table>
            <button className="close-button" onClick={() => setOpen(false)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MealDropdown;
