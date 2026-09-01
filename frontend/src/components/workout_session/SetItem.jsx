import { useState, useEffect } from "react";
import { formatTime as format, parseTime } from "../utils/time";

const now = () => Math.floor(Date.now() / 1000);

export default function SetItem({ set, index, sets, onChange, onDelete }) {
  const [, tick] = useState(0);

  // force rerender every second
  useEffect(() => {
    const interval = setInterval(() => tick(t => t + 1), 1000);
    return () => clearInterval(interval);
  }, []);

  const handleButton = () => {
    const anyWorking = sets.some((s, i) => i !== index && s.state === "working");
    if (anyWorking) {
      alert("Cannot start: another set is currently working!");
      return;
    }

    // update all resting sets to done
    sets.forEach((s, i) => {
      if (i !== index && s.state === "resting") {
        const restDur = now() - (s.restStart || now());
        const updated = { ...s, state: "done", restTime: (s.restTime || 0) + restDur, restStart: null };
        onChange(i, updated);
      }
    });

    let newSet = { ...set };
    switch (set.state) {
      case "idle":
        newSet.state = "working";
        newSet.startTime = now();
        break;

      case "working":
        const workDuration = now() - (set.startTime || now());
        newSet.state = "resting";
        newSet.workTime = (set.workTime || 0) + workDuration;
        newSet.restStart = now();
        newSet.startTime = null;
        break;

      case "resting":
        const restDuration = now() - (set.restStart || now());
        newSet.state = "done";
        newSet.restTime = (set.restTime || 0) + restDuration;
        newSet.restStart = null;
        break;

      case "done":
        if (!confirm("Redo this set? Work and rest timers will reset.")) return;
        newSet.state = "idle";
        newSet.workTime = 0;
        newSet.restTime = 0;
        newSet.startTime = null;
        newSet.restStart = null;
        break;
    }

    onChange(index, newSet);
  };

  const workTimer = () => (set.state === "working" && set.startTime ? set.workTime + (now() - set.startTime) : set.workTime || 0);
  const restTimer = () => (set.state === "resting" && set.restStart ? set.restTime + (now() - set.restStart) : set.restTime || 0);

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "40px 70px 70px 160px 120px",
      alignItems: "center",
      marginBottom: 6
    }}>
      <div>{index + 1}</div>

      <input
        type="text"
        inputMode="numeric"
        value={set.reps}
        onChange={e => onChange(index, { ...set, reps: Number(e.target.value) })}
      />
      <input
        type="text"
        inputMode="numeric"
        value={set.weight}
        onChange={e => onChange(index, { ...set, weight: Number(e.target.value) })}
      />

      <div>
        <input
          type="text"
          value={format(workTimer())}
          style={{ width: 50, marginLeft: 4 }}
          onChange={e => onChange(index, { ...set, workTime: parseTime(e.target.value) })}
        />
            <input
              type="text"
              value={format(restTimer())}
              style={{ width: 50, marginLeft: 4 }}
              onChange={e => onChange(index, { ...set, restTime: parseTime(e.target.value) })}
            />
      </div>

      <div style={{ display: "flex", gap: 4 }}>
        <button onClick={handleButton}>
          {set.state === "idle" && "Start"}
          {set.state === "working" && "Rest"}
          {set.state === "resting" && "Stop Rest"}
          {set.state === "done" && "Redo"}
        </button>
        <button onClick={() => {
          if (confirm("Delete this set?")) onDelete(index);
        }}>x</button>
      </div>
    </div>
  );
}