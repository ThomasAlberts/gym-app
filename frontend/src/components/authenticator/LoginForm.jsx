// src/components/auth/LoginForm.jsx
import React, { useState } from "react";
import { useAuth } from "./AuthContext.jsx";
import * as auth from "../../api/auth";
import ForgotPasswordForm from "./ForgotPasswordForm";

export default function LoginForm({
  email,
  setEmail,
  password,
  setPassword,
  onSuccess,
  error,
  setError,
}) {
  const [forgotPassword, setForgotPassword] = useState(false);
  const { login } = useAuth();

  const handleLogin = async (e) => {
  e.preventDefault();
  setError("");
  try {
    const res = await auth.login(email, password);
    login(res.data.user);        // was: const { access_token, user } = res.data;
    window.dispatchEvent(new Event("authChanged"));
    onSuccess();
  } catch (err) {
    setError(err.response?.data?.detail || err.message || "Login failed");
  }
};

  if (forgotPassword) {
    return (
      <>
        <ForgotPasswordForm
          email={email}
          setEmail={setEmail}
          onSuccess={() => setForgotPassword(false)}
          error={error}
          setError={setError}
        />
        <button
          type="button"
          onClick={() => {
            setForgotPassword(false);
            setError("");
          }}
          style={{ marginTop: "0.5rem" }}
        >
          Back to Login
        </button>
      </>
    );
  }

  return (
    <form onSubmit={handleLogin} style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />

      {error && <span style={{ color: "red" }}>{error}</span>}

      <button type="submit">Login</button>

      <button
        type="button"
        onClick={() => {
          setForgotPassword(true);
          setError("");
        }}
        style={{ marginTop: "0.5rem" }}
      >
        Forgot Password?
      </button>
    </form>
  );
}