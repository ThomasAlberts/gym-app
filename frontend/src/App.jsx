// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./components/authenticator/AuthContext";
import Navbar from "./components/navbar/Navbar";
import Profile from "./pages/Profile";
import CreateWorkout from "./pages/Workout";
import Dashboard from "./pages/Dashboard";
import WorkoutSession from "./components/workout_session/WorkoutSession.jsx";
// Eventueel: Login als aparte pagina als je dat wilt

function AppInner() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/profile" element={<Profile />} />
        <Route path="/workout" element={<CreateWorkout />} />
        <Route path="/workout/:workoutId" element={<WorkoutSession />} />
        <Route path="/dashboard" element={<Dashboard />} />

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