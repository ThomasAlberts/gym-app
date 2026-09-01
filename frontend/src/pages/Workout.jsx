import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios"; // pas dit pad aan naar waar jouw axios instance daadwerkelijk staat

export default function CreateWorkout() {
  const navigate = useNavigate();
  const [starting, setStarting] = useState(false);

  const startWorkout = async () => {
    setStarting(true);
    try {
      const { data } = await api.post("/workout/create_new", {
        started_at: new Date().toISOString(),
        ended_at: null,
        exercises: [],
      });
      navigate(`/workout/${data.id}`);
    } catch (e) {
      console.error(e);
      alert("Kon workout niet starten.");
      setStarting(false);
    }
  };

  return (
    <>
      <h2>Workout time 💪🏋️‍♀️</h2>
      <button onClick={startWorkout} disabled={starting}>
        {starting ? "Starten..." : "Start Workout Session"}
      </button>
    </>
  );
}