import { useNavigate, useParams } from "react-router-dom";
import useWorkoutPlanner from "./useWorkoutPlanner.js";
import PlanExerciseList from "./PlanExerciseList.jsx";
import AddExerciseForm from "../shared/AddExerciseForm.jsx";

export default function WorkoutPlanEditor() {
  const { planId } = useParams();
  const navigate = useNavigate();

  const {
    plan,
    loading,
    loadError,
    saving,
    updateName,
    updateExercises,
    savePlan,
    deletePlan,
    startPlan,
  } = useWorkoutPlanner(planId);

  const handleSave = async () => {
    try {
      const id = await savePlan();
      if (!planId || planId === "new") navigate(`/workout/plan/${id}`, { replace: true });
      else alert("Plan saved!");
    } catch (e) {
      console.error(e);
      alert("Couldn't save plan.");
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Delete this plan?")) return;
    try {
      await deletePlan();
    } catch (e) {
      console.error(e);
    }
    navigate("/workout/plans");
  };

  const handleStart = async () => {
    if (!plan.exercises.length) {
      alert("Add at least one exercise before starting.");
      return;
    }
    try {
      const id = await startPlan();
      navigate(`/workout/${id}`);
    } catch (e) {
      console.error(e);
      alert("Couldn't start workout.");
    }
  };

  if (loading || !plan) return <p>Loading plan…</p>;
  if (loadError) return <p style={{ color: "crimson" }}>Couldn't load this plan.</p>;

  return (
    <div>
      <h2>{planId && planId !== "new" ? "Edit Workout Plan" : "New Workout Plan"}</h2>
      <input
        type="text"
        value={plan.name}
        onChange={(e) => updateName(e.target.value)}
        placeholder="Plan name (e.g. Push Day)"
        style={{
          fontSize: 18,
          fontWeight: 600,
          marginBottom: 12,
          width: "100%",
          boxSizing: "border-box",
        }}
      />

      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        <button onClick={handleSave} disabled={saving}>
          {saving ? "Saving…" : "Save Plan"}
        </button>
        <button onClick={handleStart} disabled={saving}>
          Start Workout Now
        </button>
        {plan.planId && (
          <button onClick={handleDelete} style={{ backgroundColor: "red", color: "white" }}>
            Delete Plan
          </button>
        )}
      </div>

      <PlanExerciseList exercises={plan.exercises} onChange={updateExercises} />

      <AddExerciseForm
        currentWorkoutId={plan.planId}
        onAdd={(exercise) => updateExercises([...plan.exercises, exercise])}
      />
    </div>
  );
}
