import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./Pages/App.jsx";
import About from "./Pages/About.jsx"; // your new page
import LandingPage from "./Pages/LangingPage.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/about" element={<About />} />
      <Route path="/app" element={<App />} />
    </Routes>
  </BrowserRouter>
);
