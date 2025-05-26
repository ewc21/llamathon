import React, { useState } from "react";
import LlamaLogo from "../assets/LlamaLogo.png";
import "../Styles/AuthPage.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const LoginPage = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      const response = await axios.post("http://localhost:8000/login", {
        username,
        password,
      });

      console.log("Login success:", response.data);
      navigate("/dashboard");
    } catch (error) {
      const msg = error.response?.data?.detail || "Login failed";
      console.error("Login failed:", msg);
      setErrorMsg(msg);
    }
  };

  return (
    <div className="auth-container">
      <h1 className="title">GemiNutrition</h1>
      <img src={LlamaLogo} alt="Llama Logo" className="llama-logo" />
      <form className="auth-form" onSubmit={handleLogin}>
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
        {errorMsg && <p className="error-message">{errorMsg}</p>}
        <button className="action-button" type="submit">
          Login
        </button>
        <p className="link-text" onClick={() => navigate("/create-account")}>
          Don’t have an account? Create one
        </p>
      </form>
    </div>
  );
};

export default LoginPage;
