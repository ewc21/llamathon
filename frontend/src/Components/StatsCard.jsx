import React, { useRef, useLayoutEffect } from "react";
import "../Styles/StatsCard.css";

const StatsCard = ({
  label,
  currentValue,
  goalValue,
  width = 600,
  height = 180,
  minFontSize = 12,
  maxFontSize = 64,
}) => {
  const currentRef = useRef(null);
  const goalRef = useRef(null);

  const units = {
    Calories: "",
    Protein: "g",
    Carbs: "g",
    Fat: "g",
    Fiber: "g",
    Sugar: "g",
    Sodium: "mg",
    Potassium: "mg",
    Cholesterol: "mg",
    VitaminA: "%",
    VitaminC: "%",
    Calcium: "%",
    Iron: "%",
  };

  useLayoutEffect(() => {
    const refs = [currentRef, goalRef];

    refs.forEach((ref) => {
      const container = ref.current?.closest(".calorie-block");
      const text = ref.current;
      if (!container || !text) return;

      let fontSize = maxFontSize;
      text.style.fontSize = fontSize + "px";

      while (
        fontSize > minFontSize &&
        text.scrollWidth > container.clientWidth
      ) {
        fontSize -= 1;
        text.style.fontSize = fontSize + "px";
      }
    });
  }, [currentValue, goalValue, maxFontSize, minFontSize]);

  return (
    <div
      className="calorie-box"
      style={{ width: `${width}px`, height: `${height}px` }}
    >
      <div className="calorie-title">{label}</div>
      <div className="calorie-value-wrapper">
        <div className="calorie-row">
          <div className="calorie-block">
            <div className="calorie-subtitle">Current</div>
            <div ref={currentRef} className="calorie-value">
              {currentValue}
              {units[label]}
            </div>
          </div>
          <div className="calorie-block">
            <div className="calorie-subtitle">Goal</div>
            <div ref={goalRef} className="calorie-value">
              {goalValue}
              {units[label]}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsCard;
