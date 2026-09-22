import { useEffect, useState } from "react";
import { formatTime } from "../../utils/time.js";

/**
 * Displays live session time plus total work/rest across all sets.
 * Purely presentational — takes the session's startTime/pausedAt and the
 * exercises list as props, and ticks its own re-render every second.
 */
export default function WorkoutTimer({ startTime, pausedAt, exercises }) {
  const [, forceUpdate] = useState(0);

  useEffect(() => {
    if (!startTime || pausedAt) return; // don't tick while paused
    const id = setInterval(() => forceUpdate((n) => n + 1), 1000);
    return () => clearInterval(id);
  }, [startTime, pausedAt]);

  const elapsed = startTime
    ? Math.floor(((pausedAt || Date.now()) - startTime) / 1000)
    : 0;

  const totals = (exercises || []).reduce(
    (t, ex) => {
      (ex.exercise_sets || []).forEach((set) => {
        let work = set.workTime || 0;
        if (set.state === "working" && set.startTime) {
          work += Math.floor(Date.now() / 1000) - set.startTime;
        }
        let rest = set.restTime || 0;
        if (set.state === "resting" && set.restStart) {
          rest += Math.floor(Date.now() / 1000) - set.restStart;
        }
        t.work += work;
        t.rest += rest;
      });
      return t;
    },
    { work: 0, rest: 0 }
  );

  return (
    <div style={{ marginBottom: 12 }}>
      <div>
        <strong>Session Time:</strong> {formatTime(elapsed)}
        {pausedAt ? " (Paused)" : ""}
      </div>
      <div>
        <strong>Total Work:</strong> {formatTime(totals.work)} |{" "}
        <strong>Total Rest:</strong> {formatTime(totals.rest)}
      </div>
    </div>
  );
}