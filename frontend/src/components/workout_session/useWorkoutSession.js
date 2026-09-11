import { useState, useEffect, useCallback } from "react";
import api from "../../api/axios";

const parseServerDate = (value) => {
  if (value == null) return null;
  const hasTimezone = /Z$|[+-]\d{2}:?\d{2}$/.test(value);
  return new Date(hasTimezone ? value : `${value}Z`).getTime();
};

const draftKey = (workoutId) => `workout_draft_${workoutId}`;

const loadDraft = (workoutId) => {
  try {
    const raw = localStorage.getItem(draftKey(workoutId));
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    console.error("Couldn't read draft from localStorage", e);
    return null;
  }
};

const saveDraft = (workoutId, session) => {
  try {
    localStorage.setItem(draftKey(workoutId), JSON.stringify(session));
  } catch (e) {
    console.error("Couldn't write draft to localStorage", e);
  }
};

const clearDraft = (workoutId) => {
  try {
    localStorage.removeItem(draftKey(workoutId));
  } catch (e) {
    console.error("Couldn't clear draft from localStorage", e);
  }
};

const shapeSession = (data, defsById) => {
  const exercises = (data.exercises || []).map((ex) => {
    const def = defsById.get(ex.exercise_definition_id);
    return {
      ...ex,
      name: ex.name ?? def?.name ?? "Onbekende oefening",
      equipment_type: ex.equipment_type ?? def?.equipment_type ?? "machine",
      handle_type: ex.handle_type ?? def?.grip_type ?? "none",
      exercise_sets: (ex.exercise_sets || []).map((s) => ({
        ...s,
        id: s.id ?? `set_${Date.now()}_${Math.random()}`,
        state: s.state || "done",
      })),
    };
  });

  return {
    workoutId: data.id,
    name: data.name || "",
    startTime: parseServerDate(data.started_at),
    pausedAt: null,
    exercises,
  };
};

const buildPayload = (session, isFinal) => ({
  name: session.name || null,
  started_at: new Date(session.startTime).toISOString(),
  ended_at: isFinal ? new Date().toISOString() : null,
  exercises: session.exercises.map((ex) => ({
    exercise_definition_id: ex.exercise_definition_id,
    notes: ex.notes || null,
    exercise_sets: (ex.exercise_sets || []).map((s) => ({
      reps: s.reps,
      weight: s.weight,
      workTime: s.workTime || 0,
      restTime: s.restTime || 0,
    })),
  })),
});

export default function useWorkoutSession(workoutId) {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      setLoadError(null);

      // 1. Check for a local draft first — this is what survives a refresh.
      const draft = loadDraft(workoutId);
      if (draft && !cancelled) {
        setSession(draft);
        setLoading(false);
        return; // trust the draft; don't overwrite with server state
      }

      // 2. No draft — fetch fresh from the server as before.
      try {
        const [{ data }, defsRes] = await Promise.all([
          api.get(`/workout/${workoutId}`),
          api.get(`/exercise_info/exercise_defintion/all`),
        ]);
        if (cancelled) return;

        const defsById = new Map((defsRes.data || []).map((d) => [d.id, d]));
        const shaped = shapeSession(data, defsById);
        setSession(shaped);
        saveDraft(workoutId, shaped);
      } catch (e) {
        console.error(e);
        if (!cancelled) setLoadError(e);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    load();
    return () => {
      cancelled = true;
    };
  }, [workoutId]);

  // Keep localStorage in sync with every in-memory change — cheap, local, no network.
  useEffect(() => {
    if (session) saveDraft(session.workoutId, session);
  }, [session]);

  const persist = useCallback(
    async (isFinal) => {
      const payload = buildPayload(session, isFinal);
      const { data } = await api.patch(`/workout/${session.workoutId}`, payload);
      return data;
    },
    [session]
  );

  const pauseWorkout = useCallback(async () => {
    await persist(false);
    setSession((s) => ({ ...s, pausedAt: Date.now() }));
  }, [persist]);

  const resumeWorkout = useCallback(() => {
    setSession((s) => {
      if (!s?.pausedAt) return s;
      const pausedFor = Date.now() - s.pausedAt;
      return { ...s, startTime: s.startTime + pausedFor, pausedAt: null };
    });
  }, []);

  const saveWorkout = useCallback(async () => {
    const result = await persist(true);
    clearDraft(session.workoutId); // workout is finalized — draft no longer needed
    return result;
  }, [persist, session]);

  const deleteWorkout = useCallback(async () => {
    await api.delete(`/workout/${session.workoutId}`);
    clearDraft(session.workoutId);
  }, [session]);

  const updateName = useCallback((name) => {
    setSession((s) => ({ ...s, name }));
  }, []);

  const updateExercises = useCallback((exercises) => {
    setSession((s) => ({ ...s, exercises }));
  }, []);

  return {
    session,
    loading,
    loadError,
    pauseWorkout,
    resumeWorkout,
    saveWorkout,
    deleteWorkout,
    updateName,
    updateExercises,
  };
}