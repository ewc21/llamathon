import React from "react";
import LlamaLogo from "../assets/LlamaLogo.png";
import "../Styles/LandingPage.css"; // Adjust the path as necessary
import { useNavigate } from "react-router-dom";
import StatsCard from "../Components/StatsCard"; // Adjust the path as necessary
const LandingPage = () => {
  const navigate = useNavigate();
  return (
    <div className="landing-container">
      <h1 className="title">LlamaNutrition</h1>
      <img src={LlamaLogo} alt="Llama Logo" className="llama-logo" />
      <div className="button-group">
        <button className="action-button" onClick={() => navigate("/app")}>
          Login
        </button>
        <button className="action-button">Create Account</button>
      </div>
    </div>
  );
};

export default LandingPage;
