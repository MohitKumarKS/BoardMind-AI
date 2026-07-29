import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import WorkspacePage from "./pages/WorkspacePage";
import FinanceWorkspacePage from "./pages/FinanceWorkspacePage";
import AgentWorkspacePage from "./pages/AgentWorkspacePage";
import BoardroomPage from "./pages/BoardroomPage";
import ReportPage from "./pages/ReportPage";
import SessionHistoryPage from "./pages/SessionHistoryPage";
import {
  marketingConfig,
  salesConfig,
  hrConfig,
  operationsConfig,
  legalConfig,
  itConfig,
  analyticsConfig,
} from "./pages/agentConfigs";

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/workspace" element={<WorkspacePage />} />
        <Route path="/workspace/finance" element={<FinanceWorkspacePage />} />
        <Route path="/workspace/marketing" element={<AgentWorkspacePage config={marketingConfig} />} />
        <Route path="/workspace/sales" element={<AgentWorkspacePage config={salesConfig} />} />
        <Route path="/workspace/hr" element={<AgentWorkspacePage config={hrConfig} />} />
        <Route path="/workspace/operations" element={<AgentWorkspacePage config={operationsConfig} />} />
        <Route path="/workspace/legal" element={<AgentWorkspacePage config={legalConfig} />} />
        <Route path="/workspace/it" element={<AgentWorkspacePage config={itConfig} />} />
        <Route path="/workspace/business_analytics" element={<AgentWorkspacePage config={analyticsConfig} />} />
        <Route path="/boardroom" element={<BoardroomPage />} />
        <Route path="/report/:sessionId" element={<ReportPage />} />
        <Route path="/history" element={<SessionHistoryPage />} />
      </Route>
    </Routes>
  );
}

export default App;
