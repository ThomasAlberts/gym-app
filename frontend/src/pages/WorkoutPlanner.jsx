import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios.js";

export default function WorkoutPlanner() {
  const navigate = useNavigate();
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const { data } = await api.get("/workout/all");
        if (!cancelled) setWorkouts(data || []);
      } catch (e) {
        console.error(e);
        if (!cancelled) setError("Couldn't load workouts.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const plans = workouts.filter((w) => !w.started_at);
  const inProgress = workouts.filter((w) => w.started_at && !w.ended_at);
  const completed = workouts.filter((w) => w.started_at && w.ended_at);

  const renderRow = (w, onClick, label) => (
    <div
      key={w.id}
      onClick={onClick}
      style={{
        border: "1px solid #e0e0e0",
        borderRadius: 4,
        padding: "10px 12px",
        marginBottom: 8,
        cursor: "pointer",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <div>
        <strong>{w.name || "Untitled workout"}</strong>
        <div style={{ fontSize: 12, color: "#888" }}>
          {(w.exercises || []).length} exercise{(w.exercises || []).length === 1 ? "" : "s"}
        </div>
      </div>
      <span style={{ fontSize: 12, color: "#888" }}>{label}</span>
    </div>
  );

  if (loading) return <p>Loading workouts…</p>;
  if (error) return <p style={{ color: "crimson" }}>{error}</p>;

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
        }}
      >
        <h2>Workouts</h2>
        <button onClick={() => navigate("/workout/plan/new")}>+ New Plan</button>
      </div>

      {inProgress.length > 0 && (
        <>
          <h3>In Progress</h3>
          {inProgress.map((w) => renderRow(w, () => navigate(`/workout/${w.id}`), "Continue →"))}
        </>
      )}

      <h3>Plans</h3>
      {plans.length === 0 ? (
        <p style={{ fontSize: 13, color: "#888" }}>
          No plans yet — create one to prep a workout ahead of time.
        </p>
      ) : (
        plans.map((w) => renderRow(w, () => navigate(`/workout/plan/${w.id}`), "Edit / Start →"))
      )}

      {completed.length > 0 && (
        <>
          <h3>Completed</h3>
          {completed.map((w) => renderRow(w, () => navigate(`/workout/${w.id}`), "View"))}
        </>
      )}
    </div>
  );
}
