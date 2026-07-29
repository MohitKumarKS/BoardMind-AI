import { useParams } from "react-router-dom";
import "./Pages.css";

function ReportPage() {
  const { sessionId } = useParams<{ sessionId: string }>();

  return (
    <div className="page">
      <h1 className="page__title">Deliberation Report</h1>
      <p className="page__subtitle">Session: {sessionId}</p>

      <div className="page__placeholder">
        <p>Generated report content will be displayed here.</p>
      </div>
    </div>
  );
}

export default ReportPage;
