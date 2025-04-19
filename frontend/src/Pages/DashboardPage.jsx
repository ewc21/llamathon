import React, { useState } from "react";
import StatsCard from "../Components/StatsCard";
import LlamaLogo from "../assets/LlamaLogo.png";
import ChatWindow from "../Components/ChatWindow";
import "../Styles/DashboardPage.css";

const DashboardPage = () => {
  const [stats] = useState({
    Calories: { current: 1750000, goal: 2000 },
    Protein: { current: 75, goal: 100 },
    Carbs: { current: 200, goal: 250 },
    Fat: { current: 60, goal: 70 },
  });

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <img src={LlamaLogo} alt="Llama Logo" className="dashboard-logo" />
      </header>

      <div className="dashboard-content">
        <div className="chat-panel">
          <ChatWindow />
        </div>
        <div className="stats-panel">
          {Object.entries(stats).map(([label, { current, goal }]) => (
            <StatsCard
              key={label}
              label={label}
              currentValue={current}
              goalValue={goal}
              width={300}
              height={180}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
