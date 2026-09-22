import SetItem from "./SetItem.jsx";

export default function SetList({ sets, onChange }) {
  const emptySet = { reps: 0, weight: 0, state: "idle", workTime: 0, restTime: 0 };

  // Called by SetItem to update a single set
  const updateSet = (index, updatedSet) => {
    const newSets = sets.map((s, i) => {
      // If starting a set, finish other resting sets
      if (i !== index && updatedSet.state === "working" && s.state === "resting") {
        const restDur = Math.floor(Date.now() / 1000) - (s.restStart || Math.floor(Date.now() / 1000));
        return { ...s, state: "done", restTime: (s.restTime || 0) + restDur, restStart: null };
      }
      return i === index ? updatedSet : s;
    });

    onChange(newSets);
  };

  const deleteSet = (index) => onChange(sets.filter((_, i) => i !== index));

  const addSet = () => {
    const lastWeight = sets.length ? sets[sets.length - 1].weight : 0;
    onChange([...sets, { ...emptySet, weight: lastWeight }]);
  };

  const createPreset = (count, reps) => {
    const lastWeight = sets.length ? sets[sets.length - 1].weight : 0;
    const newSets = Array.from({ length: count }, () => ({ ...emptySet, reps, weight: lastWeight }));
    onChange(newSets);
  };

  const emptyAllSets = () => {
    if (window.confirm("Are you sure you want to clear all sets?")) {
      onChange([]);
    }
  };

  return (
    <div>
      {/* Preset buttons */}
      <div style={{ display: "flex", gap: 6, marginBottom: 12, flexWrap: "wrap" }}>
        <button onClick={() => createPreset(3, 5)}>3×5</button>
        <button onClick={() => createPreset(3, 8)}>3×8</button>
        <button onClick={() => createPreset(3, 10)}>3×10</button>
        <button onClick={() => createPreset(3, 12)}>3×12</button>
        <button onClick={() => createPreset(5, 5)}>5×5</button>
      </div>

      {/* Set items */}
      {sets.map((set, i) => (
        <SetItem
          key={i}
          set={set}
          index={i}
          sets={sets}
          onChange={updateSet}
          onDelete={() => deleteSet(i)}
        />
      ))}

      <div style={{ marginTop: 8, display: "flex", gap: 8 }}>
        <button onClick={addSet}>Add Set</button>
        <button onClick={emptyAllSets}>Clear All Sets</button>
      </div>
    </div>
  );
}