// SuggestExercise.jsx
import { useState } from "react";
import api from "../../../api/axios.js";

const buildPayload = (exercises) => ({
  current_exercises: (exercises || []).map((ex) => ({
    name: ex.name,
    equipment_type: ex.equipment_type,
    grip_type: ex.handle_type || "none",
    exercise_sets: (ex.exercise_sets || []).map((s) => ({
      reps: s.reps,
      weight: s.weight,
    })),
  })),
  exclude_definition_ids: (exercises || [])
    .map((ex) => ex.exercise_definition_id)
    .filter(Boolean),
});

export default function SuggestExercise({ exercises, onAdd }) {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSuggestions = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.post(
        "/exercise_info/exercise/suggest",
        buildPayload(exercises)
      );
      setSuggestions(res.data || []);
    } catch (e) {
      console.error(e);
      setError("Couldn't get a suggestion right now.");
    } finally {
      setLoading(false);
    }
  };

  const addSuggestion = (def) => {
    onAdd({
      id: `ex_${Date.now()}_${Math.random().toString(36).slice(2)}`,
      name: def.name,
      equipment_type: def.equipment_type,
      handle_type: def.grip_type || "none",
      exercise_definition_id: def.id,
      exercise_sets: [],
    });
    setSuggestions((prev) => prev.filter((d) => d.id !== def.id));
  };

  return (
    <div style={{ marginTop: 12 }}>
      <button onClick={fetchSuggestions} disabled={loading || !exercises?.length}>
        {loading ? "Thinking…" : "Suggest Next Exercise"}
      </button>

      {error && (
        <div style={{ fontSize: 12, color: "crimson", marginTop: 6 }}>{error}</div>
      )}

      {suggestions.map((def) => (
        <div
          key={def.id}
          style={{
            border: "1px solid #e0e0e0",
            borderRadius: 4,
            padding: 8,
            marginTop: 8,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: 12,
          }}
        >
          <div>
            <strong>{def.name}</strong>
            <div style={{ fontSize: 12, color: "#888" }}>
              {def.equipment_type}
              {def.grip_type && def.grip_type !== "none" ? ` · ${def.grip_type}` : ""}
            </div>
            {def.reason && (
              <div style={{ fontSize: 12, marginTop: 4 }}>{def.reason}</div>
            )}
          </div>
          <button onClick={() => addSuggestion(def)}>Add</button>
        </div>
      ))}
    </div>
  );
}