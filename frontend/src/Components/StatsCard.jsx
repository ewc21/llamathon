import React, { useRef, useLayoutEffect } from "react";
import "../Styles/StatsCard.css";

const StatsCard = ({
  label,
  value,
  width = 300,
  height = 180,
  minFontSize = 12,
  maxFontSize = 100,
}) => {
  const containerRef = useRef(null);
  const textRef = useRef(null);
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
    const container = containerRef.current;
    const text = textRef.current;
    if (!container || !text) return;

    let fontSize = maxFontSize;
    text.style.fontSize = fontSize + "px";

    while (fontSize > minFontSize && text.scrollWidth > container.clientWidth) {
      fontSize -= 1;
      text.style.fontSize = fontSize + "px";
    }
  }, [value, maxFontSize, minFontSize]);

  return (
    <div
      ref={containerRef}
      className="calorie-box"
      style={{ width: `${width}px`, height: `${height}px` }}
    >
      <div className="calorie-title">{label}</div>
      <div ref={textRef} className="calorie-value">
        {value}
        {units[label]}
      </div>
    </div>
  );
};

export default StatsCard;
