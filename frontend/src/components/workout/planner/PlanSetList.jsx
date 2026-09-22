import AddSetRow from "../shared/AddSetRow.jsx";

export default function PlanSetList({ sets, onChange }) {
  const emptySet = { reps: 0, weight: 0 };

  const updateSet = (index, field, value) => {
    onChange(sets.map((s, i) => (i === index ? { ...s, [field]: value } : s)));
  };

  const deleteSet = (index) => onChange(sets.filter((_, i) => i !== index));

  const addSet = (set) => {
    const lastWeight = sets.length ? sets[sets.length - 1].weight : 0;
    onChange([...sets, { reps: set.reps ?? 0, weight: set.weight ?? lastWeight }]);
  };

  const createPreset = (count, reps) => {
    const lastWeight = sets.length ? sets[sets.length - 1].weight : 0;
    onChange(Array.from({ length: count }, () => ({ ...emptySet, reps, weight: lastWeight })));
  };

  const emptyAllSets = () => {
    if (sets.length && !window.confirm("Clear all planned sets?")) return;
    onChange([]);
  };

  return (
    <div>
      <div style={{ display: "flex", gap: 6, marginBottom: 10, flexWrap: "wrap" }}>
        <button onClick={() => createPreset(3, 5)}>3×5</button>
        <button onClick={() => createPreset(3, 8)}>3×8</button>
        <button onClick={() => createPreset(3, 10)}>3×10</button>
        <button onClick={() => createPreset(3, 12)}>3×12</button>
        <button onClick={() => createPreset(5, 5)}>5×5</button>
      </div>

      {sets.map((set, i) => (
        <div
          key={i}
          style={{
            display: "grid",
            gridTemplateColumns: "24px 70px 70px 32px",
            gap: 6,
            alignItems: "center",
            marginBottom: 6,
          }}
        >
          <div style={{ fontSize: 12, color: "#888" }}>{i + 1}</div>
          <input
            type="text"
            inputMode="numeric"
            value={set.reps}
            onChange={(e) => updateSet(i, "reps", Number(e.target.value) || 0)}
            placeholder="Reps"
          />
          <input
            type="text"
            inputMode="numeric"
            value={set.weight}
            onChange={(e) => updateSet(i, "weight", Number(e.target.value) || 0)}
            placeholder="Weight"
          />
          <button onClick={() => deleteSet(i)}>x</button>
        </div>
      ))}

      <div style={{ marginTop: 8, display: "flex", gap: 8, alignItems: "center" }}>
        <AddSetRow onAdd={addSet} />
        {sets.length > 0 && <button onClick={emptyAllSets}>Clear All</button>}
      </div>
    </div>
  );
}
