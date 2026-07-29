import "./Pages.css";

function SessionHistoryPage() {
  return (
    <div className="page">
      <h1 className="page__title">Session History</h1>
      <p className="page__subtitle">
        View past deliberation sessions and their outcomes.
      </p>

      <div className="page__placeholder">
        <p>Session list will be displayed here.</p>
      </div>
    </div>
  );
}

export default SessionHistoryPage;
