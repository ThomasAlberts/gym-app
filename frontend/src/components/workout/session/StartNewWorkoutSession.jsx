import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../../api/axios.js";

export default function StartNewWorkoutSession() {
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
        <button onClick={startWorkout} disabled={starting}>
          {starting ? "Starten..." : "Start new workout session"}
        </button>
  );
}