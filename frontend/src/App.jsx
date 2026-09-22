// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./components/authenticator/AuthContext";
import Navbar from "./components/navbar/Navbar";
import Profile from "./pages/Profile";
import CreateWorkout from "./pages/Workout";
import Dashboard from "./pages/Dashboard";
import WorkoutSession from "./components/workout/session/WorkoutSession.jsx";
import MuscleMap from "./pages/MuscleMap.jsx";
import WorkoutPlanEditor from "./components/workout/planner/WorkoutPlanEditor.jsx";
import WorkoutPlanner from "./pages/WorkoutPlanner.jsx";
// Eventueel: Login als aparte pagina als je dat wilt

function AppInner() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/profile" element={<Profile />} />
        <Route path="/workout" element={<CreateWorkout />} />
        <Route path="/workout/:workoutId" element={<WorkoutSession />} />
        <Route path="/workout/planner" element={<WorkoutPlanner />} />
        <Route path="/workout/plan/new" element={<WorkoutPlanEditor />} />
        <Route path="/workout/plan/:planId" element={<WorkoutPlanEditor />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/muscle_map" element={<MuscleMap />} />

        <Route path="/" element={<Navigate to="/workout" replace />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppInner />
      </AuthProvider>
    </BrowserRouter>
  );
}