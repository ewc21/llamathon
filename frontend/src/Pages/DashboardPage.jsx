import React, { useState, useEffect, useCallback } from "react";
import MealSection from "../Components/MealSection";
import DailyOverview from "../Components/DailyOverview";
import LlamaLogo from "../assets/LlamaLogo.png";
import "../Styles/DashboardPage.css";

const USER_ID = 1; // TODO: replace with real user id once auth is wired
const POLL_MS = 10_000; // background refresh every 10 s

const DashboardPage = () => {
  /* ────────────────────────── state ────────────────────────── */
  const [breakfastItems, setBreakfastItems] = useState([]);
  const [lunchItems, setLunchItems] = useState([]);
  const [dinnerItems, setDinnerItems] = useState([]);
  const [snackItems, setSnackItems] = useState([]);

  const [dailyTotals, setDailyTotals] = useState({
    calories: 0,
    protein: 0,
    carbohydrates: 0,
    fat: 0,
    fiber: 0,
    sodium: 0,
  });

  /* ───────────────── fetch ALL items helper ───────────────── */
  const fetchAllMeals = useCallback(async () => {
    try {
      const res = await fetch(`http://localhost:8000/meals`);
      if (!res.ok) {
        console.error("Fetch meals error:", res.statusText);
        return;
      }
      const { meal_items } = await res.json();

      // bucket by meal_type
      const b = [],
        l = [],
        d = [],
        s = [];
      meal_items.forEach((m) => {
        switch (m.meal_type) {
          case "breakfast":
            b.push(m);
            break;
          case "lunch":
            l.push(m);
            break;
          case "dinner":
            d.push(m);
            break;
          case "snacks":
            s.push(m);
            break;
        }
      });
      setBreakfastItems(b);
      setLunchItems(l);
      setDinnerItems(d);
      setSnackItems(s);
    } catch (e) {
      console.error("Fetch meals failed:", e);
    }
  }, []);

  /* initial + polling */
  useEffect(() => {
    fetchAllMeals(); // run once on mount
    const id = setInterval(fetchAllMeals, POLL_MS);
    return () => clearInterval(id); // cleanup
  }, [fetchAllMeals]);

  /* ───────────── handle manual “Log” submit ───────────── */
  const handleLogSubmit = async (mealType, inputText) => {
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: inputText }),
      });
      if (!response.ok) return { success: false };

      const data = await response.json();
      const parsed = JSON.parse(data.response);

      const analysis = parsed.health_analysis || {};
      const newItems = (parsed.meal_items || []).map((item, idx) => ({
        ...item,
        health_analysis: analysis,
        _id: `${Date.now()}-${idx}`, // unique key for React
      }));

      // optimistic UI update
      switch (mealType) {
        case "breakfast":
          setBreakfastItems((prev) => [...prev, ...newItems]);
          break;
        case "lunch":
          setLunchItems((prev) => [...prev, ...newItems]);
          break;
        case "dinner":
          setDinnerItems((prev) => [...prev, ...newItems]);
          break;
        case "snacks":
          setSnackItems((prev) => [...prev, ...newItems]);
          break;
      }

      /* 🔥 immediately re‑sync from DB */
      await fetchAllMeals();

      return { success: true, messages: [] };
    } catch (err) {
      console.error("Request failed:", err);
      return { success: false };
    }
  };

  /* ───────────── recompute daily totals ───────────── */
  useEffect(() => {
    const all = [
      ...breakfastItems,
      ...lunchItems,
      ...dinnerItems,
      ...snackItems,
    ];
    const totals = all.reduce(
      (acc, item) => ({
        calories: acc.calories + (item.calories ?? item.macros?.calories ?? 0),
        protein: acc.protein + (item.protein ?? item.macros?.protein ?? 0),
        carbohydrates:
          acc.carbohydrates +
          (item.carbohydrates ?? item.macros?.carbohydrates ?? 0),
        fat: acc.fat + (item.fat ?? item.macros?.fat ?? 0),
        fiber: acc.fiber + (item.fiber ?? item.micros?.fiber ?? 0),
        sodium: acc.sodium + (item.sodium ?? item.micros?.sodium ?? 0),
      }),
      { calories: 0, protein: 0, carbohydrates: 0, fat: 0, fiber: 0, sodium: 0 }
    );
    setDailyTotals(totals);
  }, [breakfastItems, lunchItems, dinnerItems, snackItems]);

  /* ────────────────────────── UI ────────────────────────── */
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <img src={LlamaLogo} alt="Llama Logo" className="dashboard-logo" />
      </header>

      <div className="dashboard-content">
        <div className="meal-sections-panel">
          <MealSection
            title="Breakfast"
            mealType="breakfast"
            items={breakfastItems}
            onLogSubmit={handleLogSubmit}
          />
          <MealSection
            title="Lunch"
            mealType="lunch"
            items={lunchItems}
            onLogSubmit={handleLogSubmit}
          />
          <MealSection
            title="Dinner"
            mealType="dinner"
            items={dinnerItems}
            onLogSubmit={handleLogSubmit}
          />
          <MealSection
            title="Snacks"
            mealType="snacks"
            items={snackItems}
            onLogSubmit={handleLogSubmit}
          />
        </div>

        <div className="stats-panel">
          <DailyOverview dailyTotals={dailyTotals} />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
