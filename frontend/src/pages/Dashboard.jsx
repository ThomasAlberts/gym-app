import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Dashboard() {
  const navigate = useNavigate();
  const [workouts, setWorkouts] = useState([]);
  const [allExercises, setAllExercises] = useState([]);
  const [recentExercises, setRecentExercises] = useState([]);
  const [days, setDays] = useState(7);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadAll = async (daysBack) => {
    setLoading(true);
    setError(null);
    try {
      const [workoutsRes, allExRes, recentExRes] = await Promise.all([
        api.get("/workout/all"),
        api.get("/exercise_info/exercise/all"),
      ]);
      setWorkouts(workoutsRes.data);
      setAllExercises(allExRes.data);
    } catch (e) {
      console.error(e);
      setError("Could not load dashboard data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll(days);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleDaysChange = (value) => {
    setDays(value);
    loadAll(value);
  };

  // A single set's contribution to total weight lifted.
  // Assumes each set object has `weight` and `reps` fields; falls back
  // gracefully if either is missing (e.g. bodyweight sets with no weight).
  const setWeight = (set) => (Number(set?.weight) || 0) * (Number(set?.reps) || 1);

  const getExerciseTotals = (ex) => {
    const sets = ex.exercise_sets || [];
    return {
      totalSets: sets.length,
      totalWeight: sets.reduce((sum, s) => sum + setWeight(s), 0),
    };
  };

  const getWorkoutTotals = (w) => {
    const exercises = w.exercises || [];
    return exercises.reduce(
      (acc, ex) => {
        const { totalSets, totalWeight } = getExerciseTotals(ex);
        acc.totalSets += totalSets;
        acc.totalWeight += totalWeight;
        return acc;
      },
      { totalSets: 0, totalWeight: 0 }
    );
  };

  if (loading) return <p>Loading dashboard…</p>;
  if (error) return <p style={{ color: "crimson" }}>{error}</p>;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
      <h2>Dashboard</h2>

      <section>
        <h3>All your workouts ({workouts.length})</h3>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {workouts.map((w) => {
            const { totalSets, totalWeight } = getWorkoutTotals(w);
            return (
              <div
                key={w.id}
                onClick={() => navigate(`/workout/${w.id}`)}
                style={{ border: "1px solid #ccc", padding: 8, cursor: "pointer" }}
              >
                {new Date(w.started_at).toLocaleDateString("en-GB", {
                  day: "2-digit",
                  month: "2-digit",
                  year: "2-digit",
                })}
                {w.name ? ` — ${w.name}` : ""} —{" "}
                {w.ended_at ? "completed" : "in progress / not finished"} —{" "}
                {w.exercises.length} exercises —{" "}
                {totalSets} total sets —{" "}
                {totalWeight.toLocaleString()} kg total weight
              </div>
            );
          })}
          {workouts.length === 0 && <p>No workouts yet.</p>}
        </div>
      </section>

      <section>
        <h3>All exercises ({allExercises.length})</h3>
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th style={thStyle}>Date</th>
              <th style={thStyle}>Exercise def. ID</th>
              <th style={thStyle}>Sets</th>
              <th style={thStyle}>Total Weight</th>
              <th style={thStyle}>Notes</th>
            </tr>
          </thead>
          <tbody>
            {allExercises.map((ex) => {
              const { totalSets, totalWeight } = getExerciseTotals(ex);
              return (
                <tr key={ex.id}>
                  <td style={tdStyle}>{new Date(ex.workout_started_at).toLocaleDateString()}</td>
                  <td style={tdStyle}>{ex.exercise_definition_id}</td>
                  <td style={tdStyle}>{totalSets}</td>
                  <td style={tdStyle}>{totalWeight.toLocaleString()} kg</td>
                  <td style={tdStyle}>{ex.notes || "—"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </section>
    </div>
  );
}

const thStyle = { textAlign: "left", borderBottom: "1px solid #ccc", padding: 4 };
const tdStyle = { borderBottom: "1px solid #eee", padding: 4 };