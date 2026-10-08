import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./components/authenticator/AuthContext";
import Navbar from "./components/navbar/Navbar";
import Profile from "./pages/Profile";
import CreateWorkout from "./components/workout/session/StartNewWorkoutSession.jsx";
import Dashboard from "./pages/Dashboard";
import WorkoutSession from "./pages/WorkoutSession.jsx";
import MuscleMap from "./pages/MuscleMap.jsx";
import WorkoutPlanEditor from "./components/workout/planner/WorkoutPlanEditor.jsx";
import WorkoutPlanner from "./pages/WorkoutPlanner.jsx";
import Welcome from "./pages/Welcome.jsx";
// Eventueel: Login als aparte pagina als je dat wilt

function AppInner() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/profile" element={<Profile />} />
        <Route path="/workout/:workoutId" element={<WorkoutSession />} />
        <Route path="/workout/planner" element={<WorkoutPlanner />} />
        <Route path="/workout/plan/new" element={<WorkoutPlanEditor />} />
        <Route path="/workout/plan/:planId" element={<WorkoutPlanEditor />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/muscle_map" element={<MuscleMap />} />
        <Route path="/welcome" element={<Welcome />} />
        <Route path="/" element={<Navigate to="/welcome"/>} />
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