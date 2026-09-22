import PlanExerciseItem from "./PlanExerciseItem.jsx";

export default function PlanExerciseList({ exercises, onChange }) {
  const updateExercise = (updated) => {
    onChange(exercises.map((ex) => (ex.id === updated.id ? updated : ex)));
  };

  const deleteExercise = (id) => {
    onChange(exercises.filter((ex) => ex.id !== id));
  };

  return (
    <>
      {exercises.map((ex) => (
        <PlanExerciseItem key={ex.id} exercise={ex} onChange={updateExercise} onDelete={deleteExercise} />
      ))}
    </>
  );
}
