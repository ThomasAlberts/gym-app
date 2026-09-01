// src/components/auth/RegisterForm.jsx
import React from "react";
import { useAuth } from "./AuthContext.jsx";
import * as auth from "../../api/auth";

export default function RegisterForm({
  email,
  setEmail,
  password,
  setPassword,
  password2,
  setPassword2,
  firstName,
  setFirstName,
  lastName,
  setLastName,
  onSuccess,
  error,
  setError,
}) {
  const { login } = useAuth();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    if (password !== password2) {
      setError("Passwords do not match");
      return;
    }

    try {
      const payload = {
        email,
        password,
        ...(firstName && { first_name: firstName }),
        ...(lastName && { last_name: lastName }),
      };
      await auth.register(payload);
      const res = await auth.login(email, password);
      login(res.data.user);   // was: const { access_token, user } = res.data;

      window.dispatchEvent(new Event("authChanged"));
      onSuccess();
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Registration failed");
    }
  };

  return (
    <form style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }} onSubmit={handleRegister}>
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
      <input
        type="password"
        placeholder="Confirm Password"
        value={password2}
        onChange={(e) => setPassword2(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="First Name (optional)"
        value={firstName}
        onChange={(e) => setFirstName(e.target.value)}
      />
      <input
        type="text"
        placeholder="Last Name (optional)"
        value={lastName}
        onChange={(e) => setLastName(e.target.value)}
      />

      {error && <span style={{ color: "red" }}>{error}</span>}

      <button type="submit">Register</button>
    </form>
  );
}