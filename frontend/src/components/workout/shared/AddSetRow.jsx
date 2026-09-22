import { useState } from "react";

export default function AddSetRow({ onAdd }) {
  const [reps, setReps] = useState("");
  const [weight, setWeight] = useState("");

  const submit = () => {
    onAdd({
      reps: Number(reps) || undefined,
      weight: Number(weight) || undefined,
      duration_sec: undefined,
      rest_duration_sec: undefined
    });
    setReps("");
    setWeight("");
  };

  return (
    <div>
      <input
        placeholder="Reps"
        value={reps}
        onChange={(e) => setReps(e.target.value)}
      />
      <input
        placeholder="Weight"
        value={weight}
        onChange={(e) => setWeight(e.target.value)}
      />
      <button onClick={submit}>Add Set</button>
    </div>
  );
}
