import React, { useState } from "react";
import LlamaLogo from "../assets/LlamaLogo.png";
import "../Styles/AuthPage.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const CreateAccountPage = () => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [age, setAge] = useState("");
  const [height, setHeight] = useState("");
  const [activityLevel, setActivityLevel] = useState("Light");
  const [errorMsg, setErrorMsg] = useState("");

  const handleCreateAccount = async (e) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      const response = await axios.post("http://localhost:8000/signup", {
        name,
        username,
        password,
        age: parseInt(age),
        height: parseFloat(height),
        multiplier: activityLevel,
      });

      console.log("Signup success:", response.data);
      navigate("/dashboard");
    } catch (error) {
      const msg = error.response?.data?.detail || "Signup failed";
      console.error("Signup failed:", msg);
      setErrorMsg(msg);
    }
  };

  return (
    <div className="auth-container">
      <h1 className="title">LlamaNutrition</h1>
      <img src={LlamaLogo} alt="Llama Logo" className="llama-logo" />
      <form className="auth-form" onSubmit={handleCreateAccount}>
        <input
          type="text"
          placeholder="Full Name"
          className="auth-input"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Username"
          className="auth-input"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="auth-input"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="number"
          placeholder="Age"
          className="auth-input"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />
        <input
          type="number"
          placeholder="Height (in cm)"
          className="auth-input"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
        />
        <select
          className="auth-input"
          value={activityLevel}
          onChange={(e) => setActivityLevel(e.target.value)}
        >
          <option value="Sedentary">Sedentary</option>
          <option value="Light">Lightly Active</option>
          <option value="Moderate">Moderately Active</option>
          <option value="Very">Very Active</option>
        </select>

        {errorMsg && <p className="error-message">{errorMsg}</p>}

        <button className="action-button" type="submit">
          Create Account
        </button>
        <p className="link-text" onClick={() => navigate("/login")}>
          Already have an account? Login
        </p>
      </form>
    </div>
  );
};

export default CreateAccountPage;
