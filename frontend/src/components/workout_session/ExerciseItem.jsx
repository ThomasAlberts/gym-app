import { useState, useEffect } from "react";
import SetList from "./SetList";
import PreviousInfo from "./PreviousInfo";
import { formatTime } from "../utils/time";

const LOOKBACK_DAYS = 90;

export default function ExerciseItem({
  exercise,
  onChange,
  onDelete,
  isActive = true,
  onFocus,
  currentWorkoutId
}) {
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(exercise.name);
  const [equipment, setEquipment] = useState(exercise.equipment_type || "machine");
  const [handle, setHandle] = useState(exercise.handle_type || "none");
  const [notes, setNotes] = useState(exercise.notes || "");
  const [, tick] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => tick((t) => t + 1), 1000);
    return () => clearInterval(interval);
  }, []);

  const saveEdit = () => {
    onChange({ ...exercise, name, equipment_type: equipment, handle_type: handle, notes });
    setIsEditing(false);
  };

  const saveNotes = (value) => {
    setNotes(value);
    onChange({ ...exercise, notes: value });
  };

  const updateSets = (newSets) => {
    onChange({ ...exercise, exercise_sets: newSets });
  };

  const totalWork = (exercise.exercise_sets || []).reduce((sum, s) => {
    let work = s.workTime || 0;
    if (s.state === "working" && s.startTime) work += Math.floor(Date.now() / 1000) - s.startTime;
    return sum + work;
  }, 0);

  const totalRest = (exercise.exercise_sets || []).reduce((sum, s) => {
    let rest = s.restTime || 0;
    if (s.state === "resting" && s.restStart) rest += Math.floor(Date.now() / 1000) - s.restStart;
    return sum + rest;
  }, 0);

  // --- Minimized/collapsed view ---
  if (!isActive) {
    return (
      <div
        onClick={() => onFocus && onFocus(exercise.id)}
        style={{
          border: "1px solid #ccc",
          padding: "8px 12px",
          marginBottom: 8,
          borderRadius: 4,
          cursor: "pointer",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          background: "#fafafa",
        }}
      >
        <div>
          <strong>{exercise.name}</strong>
          <span style={{ fontSize: 12, color: "#888", marginLeft: 8 }}>
            {(exercise.exercise_sets || []).length} set
            {(exercise.exercise_sets || []).length === 1 ? "" : "s"} · {exercise.equipment_type}
          </span>
        </div>
        <span style={{ fontSize: 12, color: "#888" }}>Tap to expand</span>
      </div>
    );
  }

  // --- Full/expanded view ---
  return (
    <div style={{ border: "1px solid #ccc", padding: 12, marginBottom: 16 }}>
      {isEditing ? (
        <>
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Exercise Name" />
          <select value={equipment} onChange={(e) => setEquipment(e.target.value)}>
            <option value="barbell">Barbell</option>
            <option value="dumbbell">Dumbbell</option>
            <option value="machine">Machine</option>
            <option value="cable">Cable</option>
            <option value="bodyweight">Bodyweight</option>
            <option value="kettlebell">Kettlebell</option>
          </select>
          <select value={handle} onChange={(e) => setHandle(e.target.value)}>
            <option value="none">None</option>
            <option value="lat pull down bar">Lat Pull Down Bar</option>
            <option value="close grip">Close Grip</option>
            <option value="rope">Rope</option>
          </select>
          <button onClick={saveEdit}>Save</button>
          <button onClick={() => setIsEditing(false)}>Cancel</button>
        </>
      ) : (
        <>
          <h3 style={{ margin: "0 0 2px 0" }}>{exercise.name}</h3>
          <div style={{ fontSize: 12, color: "#888", marginBottom: 8 }}>
            {exercise.equipment_type}
            {exercise.handle_type && exercise.handle_type !== "none" ? ` · ${exercise.handle_type}` : ""}
          </div>
          <button onClick={() => setIsEditing(true)}>Edit Exercise</button>
          <button onClick={() => onDelete(exercise.id)}>Delete Exercise</button>
        </>
      )}

      <PreviousInfo exerciseDefinitionId={exercise.exercise_definition_id} currentWorkoutId={currentWorkoutId} />

      <h4>Sets:</h4>
      <SetList sets={exercise.exercise_sets || []} onChange={updateSets} />

      <div style={{ marginTop: 8, fontSize: 12 }}>
        <strong>Total Work:</strong> {formatTime(totalWork)} | <strong>Total Rest:</strong> {formatTime(totalRest)}
      </div>
      <textarea
        value={notes}
        onChange={(e) => saveNotes(e.target.value)}
        placeholder="Notes (e.g. form cues, machine seat height...)"
        rows={2}
        style={{ width: "100%", marginTop: 8, boxSizing: "border-box" }}
      />
    </div>
  );
}