import { useState, useEffect, useMemo } from "react";
import api from "../../api/axios";
import PreviousInfo from "./PreviousInfo";

const LOOKBACK_DAYS = 90; // how far back to search for a previous instance

export default function AddExerciseForm({ onAdd }) {
  const [name, setName] = useState("");
  const [equipment, setEquipment] = useState("barbell");
  const [handle, setHandle] = useState("none");

  const [definitions, setDefinitions] = useState([]);
  const [loadingDefs, setLoadingDefs] = useState(true);
  const [defsError, setDefsError] = useState(null);
  const [selectedDefinitionId, setSelectedDefinitionId] = useState(null);

  useEffect(() => {
    let cancelled = false;

    const fetchDefinitions = async () => {
      setLoadingDefs(true);
      setDefsError(null);
      try {
        const res = await api.get(`/exercise_info/exercise_defintion/all`);
        if (!cancelled) setDefinitions(res.data || []);
      } catch (e) {
        console.error(e);
        if (!cancelled) setDefsError("Couldn't load exercise list.");
      } finally {
        if (!cancelled) setLoadingDefs(false);
      }
    };

    fetchDefinitions();
    return () => {
      cancelled = true;
    };
  }, []);

  const uniqueNames = useMemo(() => {
    const seen = new Set();
    return definitions.filter((d) => {
      if (seen.has(d.name)) return false;
      seen.add(d.name);
      return true;
    });
  }, [definitions]);

  const handleNameChange = (value) => {
    setName(value);

    const match = definitions.find(
      (d) => d.name.toLowerCase() === value.toLowerCase()
    );

    if (match) {
      setSelectedDefinitionId(match.id);
      setEquipment(match.equipment_type);
      setHandle(match.grip_type || "none");
    } else {
      setSelectedDefinitionId(null);
    }
  };

  const submit = () => {
    if (!name) return;
    onAdd({
      id: `ex_${Date.now()}_${Math.random().toString(36).slice(2)}`,
      name,
      equipment_type: equipment,
      handle_type: handle,
      exercise_definition_id: selectedDefinitionId,
      exercise_sets: [],
    });
    setName("");
    setEquipment("barbell");
    setHandle("none");
    setSelectedDefinitionId(null);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
        <input
          type="text"
          list="exercise-definitions"
          placeholder="Exercise Name"
          value={name}
          onChange={(e) => handleNameChange(e.target.value)}
        />
        <datalist id="exercise-definitions">
          {uniqueNames.map((d) => (
            <option key={d.id} value={d.name} />
          ))}
        </datalist>

        <button onClick={submit}>Add Exercise</button>
      </div>

      {loadingDefs && (
        <span style={{ fontSize: 12, color: "#888" }}>Loading exercise list…</span>
      )}
      {defsError && (
        <span style={{ fontSize: 12, color: "crimson" }}>{defsError}</span>
      )}
      {!loadingDefs && !defsError && (
        <span style={{ fontSize: 12, color: "#888" }}>
          {definitions.length} known exercises loaded — start typing a name to match one, or enter a new exercise.
        </span>
      )}

      <PreviousInfo exerciseDefinitionId={selectedDefinitionId} days={LOOKBACK_DAYS} />
    </div>
  );
}