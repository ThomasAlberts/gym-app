import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import useWorkoutSession from "./useWorkoutSession";
import ExerciseList from "./ExerciseList";
import AddExerciseForm from "./AddExerciseForm";
import WorkoutTimer from "./WorkoutTimer";
import SuggestExercise from "./SuggestExercise.jsx";

export default function WorkoutSession() {
  const { workoutId } = useParams();
  const navigate = useNavigate();
  const [activeExerciseId, setActiveExerciseId] = useState(null);

  const {
    session,
    loading,
    loadError,
    pauseWorkout,
    resumeWorkout,
    saveWorkout,
    deleteWorkout,
    updateName,
    updateExercises,
  } = useWorkoutSession(workoutId);

  // Default to the most recently added exercise being expanded, once per load.
  useEffect(() => {
    if (session) {
      setActiveExerciseId(session.exercises.length ? session.exercises[session.exercises.length - 1].id : null);
    }
  }, [session?.workoutId]);

  useEffect(() => {
    if (loadError) alert("Kon deze workout niet laden.");
  }, [loadError]);

  const handlePause = async () => {
    try {
      await pauseWorkout();
    } catch (e) {
      console.error(e);
      alert("Couldn't save workout progress — pause failed.");
    }
  };

  const handleSave = async () => {
    try {
      await saveWorkout();
      alert("Workout saved!");
      navigate("/dashboard");
    } catch (e) {
      console.error(e);
      alert("Save failed");
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this session?")) return;
    try {
      await deleteWorkout();
    } catch (e) {
      console.error(e);
    }
    navigate("/dashboard");
  };

  if (loading || !session) return <p>Loading workout…</p>;

  return (
    <div>
      <h2>Workout Session</h2>
      <input
        type="text"
        value={session.name}
        onChange={(e) => updateName(e.target.value)}
        placeholder="Workout name"
        style={{ fontSize: 18, fontWeight: 600, marginBottom: 8 }}
      />
      <WorkoutTimer
        startTime={session.startTime}
        pausedAt={session.pausedAt}
        exercises={session.exercises}
      />

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        {session.pausedAt ? (
          <button onClick={resumeWorkout}>Resume</button>
        ) : (
          <button onClick={handlePause}>Pause &amp; Save Progress</button>
        )}
        <button onClick={handleSave}>Save Workout</button>
        <button onClick={handleDelete} style={{ backgroundColor: "red", color: "white" }}>
          Delete Session
        </button>
      </div>

      <ExerciseList
        exercises={session.exercises}
        activeExerciseId={activeExerciseId}
        onFocusExercise={setActiveExerciseId}
        onChange={updateExercises}
        currentWorkoutId={session.workoutId}
      />

      <AddExerciseForm
        onAdd={(exercise) => {
          updateExercises([...session.exercises, exercise]);
          setActiveExerciseId(exercise.id);
        }}
        currentWorkoutId={session.workoutId}
      />
      <SuggestExercise
        exercises={session.exercises}
        onAdd={(exercise) => {
          updateExercises([...session.exercises, exercise]);
          setActiveExerciseId(exercise.id);
        }}
      />
    </div>
  );
}
