import { useState } from "react";
import PlanSetList from "./PlanSetList.jsx";
import PreviousInfo from "../shared/PreviousInfo.jsx";

export default function PlanExerciseItem({ exercise, onChange, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(exercise.name);
  const [equipment, setEquipment] = useState(exercise.equipment_type || "machine");
  const [handle, setHandle] = useState(exercise.handle_type || "none");

  const saveEdit = () => {
    onChange({ ...exercise, name, equipment_type: equipment, handle_type: handle });
    setIsEditing(false);
  };

  const updateSets = (newSets) => {
    onChange({ ...exercise, exercise_sets: newSets });
  };

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

      {!exercise.exercise_definition_id && (
        <div style={{ fontSize: 12, color: "crimson", marginTop: 6 }}>
          This name doesn't match a known exercise, so it can't be saved yet — pick one from the
          suggestions when adding it.
        </div>
      )}

      <PreviousInfo exerciseDefinitionId={exercise.exercise_definition_id} />

      <h4>Planned Sets:</h4>
      <PlanSetList sets={exercise.exercise_sets || []} onChange={updateSets} />
    </div>
  );
}
