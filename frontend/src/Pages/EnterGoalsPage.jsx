import React, { useState } from "react";
import "../Styles/AuthPage.css"; // reuse styles or make new one

const EnterGoalsPage = () => {
  const [feet, setFeet] = useState("5");
  const [inches, setInches] = useState("6");
  const [weight, setWeight] = useState("");
  const [exercise, setExercise] = useState("moderate");
  const [age, setAge] = useState("");
  const [sex, setSex] = useState("male");

  const calculateGoals = () => {
    const heightInInches = parseInt(feet) * 12 + parseInt(inches);
    const weightInKg = parseFloat(weight) * 0.453592;
    const heightInCm = heightInInches * 2.54;

    // Mifflin-St Jeor Equation
    let bmr =
      sex === "male"
        ? 10 * weightInKg + 6.25 * heightInCm - 5 * age + 5
        : 10 * weightInKg + 6.25 * heightInCm - 5 * age - 161;

    const activityFactors = {
      none: 1.2,
      light: 1.375,
      moderate: 1.55,
      active: 1.725,
      very_active: 1.9,
    };

    const calories = Math.round(bmr * activityFactors[exercise]);
    const protein = Math.round(weight * 0.8); // grams per lb
    const fat = Math.round((calories * 0.25) / 9);
    const carbs = Math.round((calories - protein * 4 - fat * 9) / 4);

    alert(`Calories: ${calories}\nProtein: ${protein}g\nFat: ${fat}g\nCarbs: ${carbs}g`);
  };

  return (
    <div className="auth-container">
      <h1 className="title">Enter Your Goals</h1>
      <form className="auth-form" onSubmit={(e) => e.preventDefault()}>
        <label>Height:</label>
        <div style={{ display: "flex", gap: "10px" }}>
          <select value={feet} onChange={(e) => setFeet(e.target.value)}>
            {[...Array(3)].map((_, i) => (
              <option key={i + 4}>{i + 4}</option>
            ))}
          </select>
          <select value={inches} onChange={(e) => setInches(e.target.value)}>
            {[...Array(12)].map((_, i) => (
              <option key={i}>{i}</option>
            ))}
          </select>
        </div>

        <input
          type="number"
          placeholder="Weight (lbs)"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
          className="auth-input"
        />
        <input
          type="number"
          placeholder="Age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          className="auth-input"
        />
        <select value={sex} onChange={(e) => setSex(e.target.value)} className="auth-input">
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
        <select value={exercise} onChange={(e) => setExercise(e.target.value)} className="auth-input">
          <option value="none">None</option>
          <option value="light">Light (1-2 days/week)</option>
          <option value="moderate">Moderate (3-5 days/week)</option>
          <option value="active">Active (6-7 days/week)</option>
          <option value="very_active">Very Active (twice/day)</option>
        </select>

        <button className="action-button" type="button" onClick={calculateGoals}>
          Calculate My Goals
        </button>
      </form>
    </div>
  );
};

export default EnterGoalsPage;
