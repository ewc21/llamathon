import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./Pages/App.jsx";
import About from "./Pages/About.jsx"; // your new page
import LandingPage from "./Pages/LandingPage.jsx";
import LoginPage from "./Pages/LoginPage.jsx";
import CreateAccountPage from "./Pages/CreateAccountPage.jsx";
import DashboardPage from "./Pages/DashboardPage.jsx";
import EnterGoalsPage from "./Pages/EnterGoalsPage.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/about" element={<About />} />
      <Route path="/app" element={<App />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/create-account" element={<CreateAccountPage />} />
      <Route path="/signup" element={<CreateAccountPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/goals" element={<EnterGoalsPage />} />
    </Routes>
  </BrowserRouter>
);
