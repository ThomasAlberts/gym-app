import ExerciseItem from "./ExerciseItem";

export default function ExerciseList({ exercises, onChange }) {
  const updateExercise = (updated) => {
    onChange(exercises.map((ex) => (ex.id === updated.id ? updated : ex)));
  };

  const deleteExercise = (id) => {
    onChange(exercises.filter((ex) => ex.id !== id));
  };

  return (
    <>
      {exercises.map((ex) => (
        <ExerciseItem
          key={ex.id}
          exercise={ex}
          onChange={updateExercise}
          onDelete={deleteExercise}
        />
      ))}
    </>
  );
}
