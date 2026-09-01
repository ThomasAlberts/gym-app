import React, { useState } from "react";
import * as auth from "../../api/auth"; // you can create a forgotPassword endpoint in your backend

export default function ForgotPasswordForm({ email, setEmail, onSuccess, error, setError }) {
  const handleForgotPassword = async (e) => {
    e.preventDefault();
    setError("");

    try {
      // Replace with your actual API call
      await auth.forgotPassword(email); // e.g., POST /auth/forgot-password
      onSuccess(); // close panel or show success message
      alert("If this email is registered, a reset link has been sent."); // temporary feedback
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Request failed");
    }
  };

  return (
    <form style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }} onSubmit={handleForgotPassword}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      {error && <span style={{ color: "red" }}>{error}</span>}
      <button type="submit">Send Reset Link</button>
    </form>
  );
}
