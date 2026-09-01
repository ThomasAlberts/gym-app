import { useState, useEffect } from "react";
import api from "../../api/axios";

const DEFAULT_LOOKBACK_DAYS = 30;

const daysAgo = (isoString) => {
  if (!isoString) return null;
  return Math.floor((Date.now() - new Date(isoString).getTime()) / (1000 * 60 * 60 * 24));
};

export default function PreviousInfo({ exerciseDefinitionId, days = DEFAULT_LOOKBACK_DAYS }) {
  const [previous, setPrevious] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!exerciseDefinitionId) {
      setPrevious(null);
      setError(null);
      return;
    }

    let cancelled = false;

    const fetchPrevious = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.get(
          `/exercise_info/exercise/last/${exerciseDefinitionId}`,
          { params: { days } }
        );
        if (!cancelled) setPrevious(res.data || null);
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
  }, [exerciseDefinitionId, days]);

  if (!exerciseDefinitionId) return null;

  if (loading) {
    return <div style={{ fontSize: 12, color: "#888", marginTop: 8 }}>Checking previous performance…</div>;
  }

  if (error) {
    return <div style={{ fontSize: 12, color: "crimson", marginTop: 8 }}>{error}</div>;
  }

  if (!previous) {
    return (
      <div style={{ fontSize: 12, color: "#888", marginTop: 8 }}>
        No record of this exercise in the last {days} days.
      </div>
    );
  }

  // Build one-line sets string, e.g. "10 reps @ 20, 8 reps @ 22.5"
  const setsLine = (previous.exercise_sets || [])
    .map((s) => {
      const repsPart = s.reps != null ? `${s.reps}` : "—";
      const weightPart = s.weight != null ? ` x ${s.weight}` : "";
      return `${repsPart}${weightPart}`;
    })
    .join(", ");

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
      <div>
        {previous.workout_started_at && (
          <span style={{ color: "#888" }}> ({daysAgo(previous.workout_started_at)} days ago)</span>
        )}
        : {setsLine}
      </div>
      
      {previous.notes && (
        <div style={{ marginTop: 4 }}>
          <em>Note: {previous.notes}</em>
        </div>
      )}
    </div>
  );
}