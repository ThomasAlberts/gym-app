import { useState, useEffect } from "react";
import api from "../../api/axios";

const DEFAULT_LOOKBACK_DAYS = 90;
const DEFAULT_LIMIT = 3;

const daysAgo = (isoString) => {
  if (!isoString) return null;
  return Math.floor((Date.now() - new Date(isoString).getTime()) / (1000 * 60 * 60 * 24));
};

const formatSetsLine = (exercise_sets) =>
  (exercise_sets || [])
    .map((s) => {
      const repsPart = s.reps != null ? `${s.reps}` : "—";
      const weightPart = s.weight != null ? ` x ${s.weight}` : "";
      return `${repsPart}${weightPart}`;
    })
    .join(", ");

export default function PreviousInfo({
  exerciseDefinitionId,
  currentWorkoutId, // id of the workout currently being logged, excluded from results
  days = DEFAULT_LOOKBACK_DAYS,
  limit = DEFAULT_LIMIT,
}) {
  const [previous, setPrevious] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!exerciseDefinitionId) {
      setPrevious([]);
      setError(null);
      return;
    }

    let cancelled = false;

    const fetchPrevious = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.get(
          `/exercise_info/exercise/last/${exerciseDefinitionId}/history`,
          {
            params: {
              days,
              limit,
              exclude_workout_id: currentWorkoutId || undefined,
            },
          }
        );
        let data = Array.isArray(res.data) ? res.data : [];

        // Safety net in case backend doesn't filter (or currentWorkoutId arrives late)
        if (currentWorkoutId != null) {
          data = data.filter(
            (d) => String(d.workout_id) !== String(currentWorkoutId)
          );
        }

        if (!cancelled) setPrevious(data.slice(0, limit));
      } catch (e) {
        console.error(e);
        if (!cancelled) setError("Couldn't load previous performance.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    fetchPrevious();
    return () => {
      cancelled = true;
    };
  }, [exerciseDefinitionId, currentWorkoutId, days, limit]);

  if (!exerciseDefinitionId) return null;

  if (loading) {
    return <div style={{ fontSize: 12, color: "#888", marginTop: 8 }}>Checking previous performance…</div>;
  }

  if (error) {
    return <div style={{ fontSize: 12, color: "crimson", marginTop: 8 }}>{error}</div>;
  }

  if (previous.length === 0) {
    return (
      <div style={{ fontSize: 12, color: "#888", marginTop: 8 }}>
        No record of this exercise in the last {days} days.
      </div>
    );
  }

  return (
    <div
      style={{
        fontSize: 12,
        background: "#f6f6f6",
        border: "1px solid #e0e0e0",
        borderRadius: 4,
        padding: 8,
        marginTop: 8,
      }}
    >
      {previous.map((entry, i) => (
        <div key={entry.id ?? i} style={{ marginTop: i === 0 ? 0 : 6 }}>
          <div>
            {entry.workout_started_at && (
              <span style={{ color: "#888" }}>
                ({daysAgo(entry.workout_started_at)} days ago)
              </span>
            )}
            : {formatSetsLine(entry.exercise_sets)}
          </div>
          {entry.notes && (
            <div style={{ marginTop: 2 }}>
              <em>Note: {entry.notes}</em>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}