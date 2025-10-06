import { useState, useEffect } from "react";
import { getBalance, withdraw, deposit, getDailyLimit } from "../api";

function Dashboard({ userName, onLogout }) {
  const [balance, setBalance] = useState(0);
  const [dailyLimit, setDailyLimit] = useState(null);
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState({ type: "", text: "" });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAccountData();
  }, []);

  const fetchAccountData = async () => {
    try {
      const [balanceRes, limitRes] = await Promise.all([
        getBalance(),
        getDailyLimit(),
      ]);

      setBalance(balanceRes.data.balance);
      setDailyLimit(limitRes.data);
    } catch (err) {
      setMessage({
        type: "error",
        text: "Failed to load account data",
      });
    }
  };

  const handleTransaction = async (type) => {
    const transactionAmount = parseFloat(amount);

    if (!transactionAmount || transactionAmount <= 0) {
      setMessage({ type: "error", text: "Please enter a valid amount" });
      return;
    }

    // Validate cents (max 2 decimal places)
    if (Math.round(transactionAmount * 100) / 100 !== transactionAmount) {
      setMessage({
        type: "error",
        text: "Amount must have at most 2 decimal places",
      });
      return;
    }

    setLoading(true);
    setMessage({ type: "", text: "" });

    try {
      const apiCall = type === "withdraw" ? withdraw : deposit;
      const response = await apiCall(transactionAmount);
      setBalance(response.data.new_balance);
      setAmount("");
      setMessage({
        type: "success",
        text: `Successfully ${
          type === "withdraw" ? "withdrew" : "deposited"
        } $${transactionAmount.toFixed(2)}`,
      });

      // Refresh daily limit
      const limitRes = await getDailyLimit();
      setDailyLimit(limitRes.data);
    } catch (err) {
      setMessage({
        type: "error",
        text:
          err.response?.data?.detail ||
          `${type === "withdraw" ? "Withdrawal" : "Deposit"} failed`,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <div className="user-info">
        <h2>👤 {userName}</h2>
      </div>

      <div className="balance-card">
        <h3>Current Balance</h3>
        <div className="balance-amount">${balance.toFixed(2)}</div>
        {dailyLimit && (
          <div className="daily-limit-info">
            <div>
              Daily Withdrawal Limit: ${dailyLimit.daily_limit.toFixed(2)}
            </div>
            <div>Withdrawn Today: ${dailyLimit.withdrawn_today.toFixed(2)}</div>
            <div>Remaining: ${dailyLimit.remaining_today.toFixed(2)}</div>
          </div>
        )}
      </div>

      {message.text && (
        <div
          className={
            message.type === "error" ? "error-message" : "success-message"
          }
        >
          {message.text}
        </div>
      )}

      <form className="transaction-form">
        <div className="input-group">
          <label htmlFor="amount">Transaction Amount</label>
          <input
            id="amount"
            type="number"
            step="0.01"
            min="0"
            placeholder="0.00"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
        </div>

        <div className="button-group">
          <button
            type="button"
            className="btn btn-danger"
            onClick={() => handleTransaction("withdraw")}
            disabled={loading || !amount}
          >
            💸 Withdraw
          </button>
          <button
            type="button"
            className="btn btn-success"
            onClick={() => handleTransaction("deposit")}
            disabled={loading || !amount}
          >
            💰 Deposit
          </button>
        </div>
      </form>

      <button className="btn btn-secondary logout-btn" onClick={onLogout}>
        Logout
      </button>
    </div>
  );
}

export default Dashboard;
