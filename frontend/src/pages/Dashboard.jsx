import { useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Dashboard() {
  const navigate = useNavigate();
  const [workouts, setWorkouts] = useState([]);
  const [allExercises, setAllExercises] = useState([]);
  const [definitions, setDefinitions] = useState([]);
  const [recentExercises, setRecentExercises] = useState([]);
  const [days, setDays] = useState(7);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadAll = async (daysBack) => {
    setLoading(true);
    setError(null);
    try {
      const [workoutsRes, allExRes, defsRes] = await Promise.all([
        api.get("/workout/all"),
        api.get("/exercise_info/exercise/all"),
        api.get("/exercise_info/exercise_defintion/all"),
      ]);
      setWorkouts(workoutsRes.data);
      setAllExercises(allExRes.data);
      setDefinitions(defsRes.data || []);
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

  const definitionById = useMemo(() => {
    const map = new Map();
    definitions.forEach((d) => map.set(d.id, d));
    return map;
  }, [definitions]);

  const getExerciseName = (ex) =>
    definitionById.get(ex.exercise_definition_id)?.name || `#${ex.exercise_definition_id}`;

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
        <ul style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexDirection: "column", gap: 6 }}>
          {allExercises.map((ex) => {
            const { totalSets, totalWeight } = getExerciseTotals(ex);
            return (
              <li key={ex.id} style={{ border: "1px solid #eee", padding: 8, borderRadius: 4 }}>
                <div>
                  <strong>{getExerciseName(ex)}</strong>{" "}
                  <span style={{ fontSize: 12, color: "#888" }}>
                    —{" "}
                    {new Date(ex.workout_started_at).toLocaleDateString("en-GB", {
                      day: "2-digit",
                      month: "2-digit",
                      year: "2-digit",
                    })}
                  </span>
                </div>
                <div style={{ fontSize: 12, color: "#888", marginTop: 2 }}>
                  {totalSets} set{totalSets === 1 ? "" : "s"} — {totalWeight.toLocaleString()} kg total weight
                </div>
                {ex.notes && (
                  <div style={{ fontSize: 12, marginTop: 2 }}>
                    <em>Note: {ex.notes}</em>
                  </div>
                )}
              </li>
            );
          })}
          {allExercises.length === 0 && <p>No exercises yet.</p>}
        </ul>
      </section>
    </div>
  );
}
