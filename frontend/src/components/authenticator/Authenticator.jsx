// src/components/auth/Authenticator.jsx
import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext.jsx";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

export default function Authenticator() {
  const navigate = useNavigate();
  const panelRef = useRef(null);
  const { isLoggedIn, logout } = useAuth();

  const [panelVisible, setPanelVisible] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");

  // Persistent form state (optioneel, kan ook lokaal in LoginForm/RegisterForm)
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  useEffect(() => {
    function handleClickOutside(event) {
      if (panelRef.current && !panelRef.current.contains(event.target)) {
        setPanelVisible(false);
        setIsRegister(false);
        setError("");
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    window.dispatchEvent(new Event("authChanged"));
    setPanelVisible(false);
    navigate("/");
  };

  const handleSuccess = () => {
    setPanelVisible(false);
    setIsRegister(false);
    setError("");
    navigate("/dashboard");
  };

  return (
    <div style={{ position: "relative" }}>
      <button onClick={() => setPanelVisible((v) => !v)}>👤</button>

      {panelVisible && (
        <div
          ref={panelRef}
          style={{
            position: "absolute",
            right: 0,
            top: "120%",
            background: "#f9f9f9",
            border: "1px solid #ccc",
            padding: "1rem",
            minWidth: "240px",
            zIndex: 1001,
          }}
        >
          {!isLoggedIn ? (
            <>
              {isRegister ? (
                <RegisterForm
                  email={email}
                  setEmail={setEmail}
                  password={password}
                  setPassword={setPassword}
                  password2={password2}
                  setPassword2={setPassword2}
                  firstName={firstName}
                  setFirstName={setFirstName}
                  lastName={lastName}
                  setLastName={setLastName}
                  onSuccess={handleSuccess}
                  error={error}
                  setError={setError}
                />
              ) : (
                <LoginForm
                  email={email}
                  setEmail={setEmail}
                  password={password}
                  setPassword={setPassword}
                  onSuccess={handleSuccess}
                  error={error}
                  setError={setError}
                />
              )}

              <button
                type="button"
                onClick={() => setIsRegister(!isRegister)}
                style={{ marginTop: "0.5rem" }}
              >
                {isRegister
                  ? "Already have an account? Login"
                  : "Don't have an account? Register"}
              </button>
            </>
          ) : (
            <button onClick={handleLogout}>Logout</button>
          )}
        </div>
      )}
    </div>
  );
}