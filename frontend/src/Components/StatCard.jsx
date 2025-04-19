import React from "react";
import "./StatCard.css";

const StatCard = ({ label, value, unit }) => {
  return (
    <div className="stat-card">
      <h2 className="stat-label">{label}</h2>
      <p className="stat-value">
        {value} {unit && <span className="stat-unit">{unit}</span>}
      </p>
    </div>
  );
};

export default StatCard;
