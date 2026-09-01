import { useState, useEffect, useCallback } from "react";
import api from "../../api/axios";

const parseServerDate = (value) => {
  if (value == null) return null;
  const hasTimezone = /Z$|[+-]\d{2}:?\d{2}$/.test(value);
  return new Date(hasTimezone ? value : `${value}Z`).getTime();
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
      try {
        const [{ data }, defsRes] = await Promise.all([
          api.get(`/workout/${workoutId}`),
          api.get(`/exercise_info/exercise_defintion/all`),
        ]);
        if (cancelled) return;

        const defsById = new Map((defsRes.data || []).map((d) => [d.id, d]));
        setSession(shapeSession(data, defsById));
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

  const saveWorkout = useCallback(() => persist(true), [persist]);

  const deleteWorkout = useCallback(async () => {
    await api.delete(`/workout/${session.workoutId}`);
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
