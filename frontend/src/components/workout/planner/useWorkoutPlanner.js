import { useState, useEffect, useCallback } from "react";
import api from "../../../api/axios";

const shapePlan = (data, defsById) => {
  const exercises = (data.exercises || []).map((ex) => {
    const def = defsById.get(ex.exercise_definition_id);
    return {
      ...ex,
      id: ex.id ?? `ex_${Date.now()}_${Math.random().toString(36).slice(2)}`,
      name: ex.name ?? def?.name ?? "Unknown exercise",
      equipment_type: ex.equipment_type ?? def?.equipment_type ?? "machine",
      handle_type: ex.handle_type ?? def?.grip_type ?? "none",
      exercise_sets: (ex.exercise_sets || []).map((s) => ({
        reps: s.reps ?? 0,
        weight: s.weight ?? 0,
      })),
    };
  });

  return {
    planId: data.id,
    name: data.name || "",
    exercises,
  };
};

// started_at is passed in explicitly: null while it's still just a plan,
// an ISO timestamp the moment it gets started.
const buildPayload = (plan, startedAt) => ({
  name: plan.name || null,
  started_at: startedAt,
  ended_at: null,
  exercises: plan.exercises.map((ex) => ({
    exercise_definition_id: ex.exercise_definition_id,
    notes: ex.notes || null,
    exercise_sets: (ex.exercise_sets || []).map((s) => ({
      reps: s.reps,
      weight: s.weight,
      work_time: 0,
      rest_time: 0,
    })),
  })),
});

const emptyPlan = { planId: null, name: "", exercises: [] };

export default function useWorkoutPlanner(planId) {
  const isNew = !planId || planId === "new";
  const [plan, setPlan] = useState(isNew ? emptyPlan : null);
  const [loading, setLoading] = useState(!isNew);
  const [loadError, setLoadError] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (isNew) {
      setPlan(emptyPlan);
      setLoading(false);
      return;
    }

    let cancelled = false;

    const load = async () => {
      setLoading(true);
      setLoadError(null);
      try {
        const [{ data }, defsRes] = await Promise.all([
          api.get(`/workout/${planId}`),
          api.get(`/exercise_info/exercise_definition/all`),
        ]);
        if (cancelled) return;
        const defsById = new Map((defsRes.data || []).map((d) => [d.id, d]));
        setPlan(shapePlan(data, defsById));
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
  }, [planId, isNew]);

  const updateName = useCallback((name) => {
    setPlan((p) => ({ ...p, name }));
  }, []);

  const updateExercises = useCallback((exercises) => {
    setPlan((p) => ({ ...p, exercises }));
  }, []);

  // Creates the plan if it doesn't exist yet, otherwise updates it in place.
  // Always keeps started_at null — use startPlan() to actually begin it.
  const savePlan = useCallback(async () => {
    setSaving(true);
    try {
      const payload = buildPayload(plan, null);
      if (isNew || !plan.planId) {
        const { data } = await api.post(`/workout/create_new`, payload);
        setPlan((p) => ({ ...p, planId: data.id }));
        return data.id;
      }
      await api.patch(`/workout/${plan.planId}`, payload);
      return plan.planId;
    } finally {
      setSaving(false);
    }
  }, [plan, isNew]);

  const deletePlan = useCallback(async () => {
    if (!plan?.planId) return;
    await api.delete(`/workout/${plan.planId}`);
  }, [plan]);

  // Saves the current plan (creating it if needed) and marks it as started
  // by setting started_at to now. Returns the workout id to navigate to —
  // from there the existing WorkoutSession page takes over unchanged.
  const startPlan = useCallback(async () => {
    setSaving(true);
    try {
      const startedAt = new Date().toISOString();
      const payload = buildPayload(plan, startedAt);
      if (isNew || !plan.planId) {
        const { data } = await api.post(`/workout/create_new`, payload);
        return data.id;
      }
      await api.patch(`/workout/${plan.planId}`, payload);
      return plan.planId;
    } finally {
      setSaving(false);
    }
  }, [plan, isNew]);

  return {
    plan,
    loading,
    loadError,
    saving,
    updateName,
    updateExercises,
    savePlan,
    deletePlan,
    startPlan,
  };
}
