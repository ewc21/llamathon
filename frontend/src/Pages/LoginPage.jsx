import React from "react";
import LlamaLogo from "../assets/LlamaLogo.png";
import "../Styles/AuthPage.css";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const navigate = useNavigate();

  return (
    <div className="auth-container">
      <h1 className="title">LlamaNutrition</h1>
      <img src={LlamaLogo} alt="Llama Logo" className="llama-logo" />
      <form className="auth-form">
        <input type="email" placeholder="Email" className="auth-input" />
        <input type="password" placeholder="Password" className="auth-input" />
        <button className="action-button">Login</button>
        <p className="link-text" onClick={() => navigate("/create-account")}>
          Don’t have an account? Create one
        </p>
      </form>
    </div>
  );
};

export default LoginPage;
