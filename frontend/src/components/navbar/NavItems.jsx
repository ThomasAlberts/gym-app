import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../authenticator/AuthContext.jsx";

// Define your nav items and allowed roles todo: move
const NAV_ITEMS = [
  { label: "Profile", path: "/profile", roles: ["user", "coach", "admin"] },
  { label: "Workout", path: "/workout", roles: ["user", "coach", "admin"] },
  { label: "Dashboard", path: "/dashboard", roles: ["user", "coach", "admin"] },
  { label: "Muscle map", path: "/muscle_map", roles: ["user", "coach", "admin"] },
  { label: "Admin Panel", path: "/admin", roles: ["admin"] },
];

export default function NavItems() {
  const navigate = useNavigate();
  const { user, isLoggedIn } = useAuth();

  const role = isLoggedIn ? user?.role ?? "anonymous" : "anonymous";

  // Filter items for the current role
  const navItems = NAV_ITEMS.filter((item) => item.roles.includes(role));

  if (navItems.length === 0) return null; // Hide component for anonymous users

  return (
    <>
      {navItems.map((item) => (
        <button
          key={item.path}
          onClick={() => navigate(item.path)}
          style={{ padding: "0.5rem 1rem" }}
        >
          {item.label}
        </button>
      ))}
    </>
  );
}
