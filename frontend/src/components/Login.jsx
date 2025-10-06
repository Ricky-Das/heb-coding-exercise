import { useState } from "react";
import { login } from "../api";

function Login({ onLoginSuccess }) {
  const [pin, setPin] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (pin.length < 4) {
      setError("PIN must be at least 4 digits");
      return;
    }

    setLoading(true);

    try {
      const response = await login(pin);
      const { token, name } = response.data;

      // Store token and user info
      localStorage.setItem("token", token);
      localStorage.setItem("userName", name);

      onLoginSuccess(name);
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid PIN. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handlePinChange = (e) => {
    const value = e.target.value.replace(/\D/g, ""); // Only digits
    if (value.length <= 6) {
      setPin(value);
    }
  };

  return (
    <div className="login-container">
      <h2>Welcome</h2>
      <p>Please enter your PIN to continue</p>

      <form onSubmit={handleSubmit}>
        {error && <div className="error-message">{error}</div>}

        <div className="pin-input-container">
          <input
            type="password"
            className="pin-input"
            placeholder="••••"
            value={pin}
            onChange={handlePinChange}
            maxLength={6}
            autoFocus
          />
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || pin.length < 4}
        >
          {loading ? "Authenticating..." : "Login"}
        </button>
      </form>

      <div className="test-pins">
        <strong>Test Accounts:</strong>
        <div>PIN: 1234 - John Doe ($5,000.00)</div>
        <div>PIN: 5678 - Jane Smith ($10,000.00)</div>
        <div>PIN: 9999 - Bob Johnson ($2,500.00)</div>
      </div>
    </div>
  );
}

export default Login;
