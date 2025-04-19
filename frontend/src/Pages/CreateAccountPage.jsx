import React from "react";
import LlamaLogo from "../assets/LlamaLogo.png";
import "../Styles/AuthPage.css";
import { useNavigate } from "react-router-dom";

const CreateAccountPage = () => {
  const navigate = useNavigate();

  return (
    <div className="auth-container">
      <h1 className="title">LlamaNutrition</h1>
      <img src={LlamaLogo} alt="Llama Logo" className="llama-logo" />
      <form className="auth-form">
        <input type="text" placeholder="Full Name" className="auth-input" />
        <input type="text" placeholder="Username" className="auth-input" />
        <input type="password" placeholder="Password" className="auth-input" />
        <button className="action-button">Create Account</button>
        <p className="link-text" onClick={() => navigate("/login")}>
          Already have an account? Login
        </p>
      </form>
    </div>
  );
};

export default CreateAccountPage;
