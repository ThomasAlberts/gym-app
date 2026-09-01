import { createContext, useContext, useState, useEffect } from "react";
import * as auth from "../../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(true);

  // Bij opstarten: check of er een geldige cookie is
  useEffect(() => {
    auth.me()
      .then((res) => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setChecking(false));
  }, []);

  useEffect(() => {
  const handleExpired = () => setUser(null);
  window.addEventListener("authExpired", handleExpired);
  return () => window.removeEventListener("authExpired", handleExpired);
}, []);

  const login = (loggedInUser) => {
    setUser(loggedInUser);
  };

  const logout = async () => {
    try {
      await auth.logout();
    } finally {
      setUser(null);
    }
  };

  const value = {
    user,
    isLoggedIn: !!user,
    checking,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}