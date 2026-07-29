import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ScenarioInput from "../components/boardroom/ScenarioInput";
import MeetingProgress, { MeetingStage } from "../components/boardroom/MeetingProgress";
import DepartmentCard from "../components/boardroom/DepartmentCard";
import ConsensusCard from "../components/boardroom/ConsensusCard";
import ConsensusCharts from "../components/boardroom/ConsensusCharts";
import ExecutiveSummary from "../components/boardroom/ExecutiveSummary";
import ExecutionTimeline from "../components/boardroom/ExecutionTimeline";
import {
  orchestrate,
  runConsensus,
  uploadFile,
  OrchestrateResponse,
  ConsensusResult,
  MCPFileResult,
} from "../services/boardroomApi";
import "./BoardroomPage.css";

const fadeSlide = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
  transition: { duration: 0.25 },
};

function BoardroomPage() {
  const [scenario, setScenario] = useState("");
  const [context, setContext] = useState("");
  const [attachedFile, setAttachedFile] = useState<File | null>(null);
  const [stage, setStage] = useState<MeetingStage>("idle");
  const [error, setError] = useState<string | null>(null);
  const [orchestrationResult, setOrchestrationResult] = useState<OrchestrateResponse | null>(null);
  const [consensus, setConsensus] = useState<ConsensusResult | null>(null);
  const [mcpData, setMcpData] = useState<MCPFileResult | null>(null);

  const handleStartMeeting = async () => {
    if (scenario.trim().length < 20) return;

    setError(null);
    setOrchestrationResult(null);
    setConsensus(null);
    setMcpData(null);
    setStage("routing");

    try {
      let fileContext = "";
      if (attachedFile) {
        const fileResult = await uploadFile(attachedFile);
        setMcpData(fileResult);
        // Use the structured evidence summary generated server-side
        const summary = (fileResult as Record<string, unknown>).evidence_summary as string | undefined;
        if (summary) {
          fileContext = `\n\n[Attached File: ${fileResult.filename}]\n${summary}`;
        } else if (fileResult.text) {
          fileContext = `\n\n[Attached File: ${fileResult.filename}]\n${fileResult.text.slice(0, 2000)}`;
        } else if (fileResult.data && fileResult.columns) {
          const preview = fileResult.data.slice(0, 5);
          fileContext = `\n\n[Attached File: ${fileResult.filename}]\nColumns: ${fileResult.columns.join(", ")}\nRows: ${fileResult.total_rows}\nPreview:\n${JSON.stringify(preview, null, 2).slice(0, 1500)}`;
        }
      }

      setStage("executing");
      const combinedContext = (context.trim() + fileContext).trim() || null;
      const orchResult = await orchestrate({
        scenario: scenario.trim(),
        optional_context: combinedContext,
      });
      setOrchestrationResult(orchResult);

      setStage("consensus");
      const consensusResult = await runConsensus(orchResult.session_id);
      setConsensus(consensusResult);

      setStage("complete");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Meeting failed");
      setStage("error");
    }
  };

  return (
    <div className="boardroom-page">
      <div className="boardroom-page__header">
        <h1 className="boardroom-page__title">Executive Boardroom</h1>
        <p className="boardroom-page__subtitle">
          Multi-department AI analysis with executive consensus
        </p>
      </div>

      <ScenarioInput
        scenario={scenario}
        context={context}
        loading={stage !== "idle" && stage !== "complete" && stage !== "error"}
        attachedFile={attachedFile}
        onScenarioChange={setScenario}
        onContextChange={setContext}
        onFileAttach={setAttachedFile}
        onSubmit={handleStartMeeting}
      />

      <MeetingProgress
        stage={stage}
        category={orchestrationResult?.business_category}
        agentCount={orchestrationResult?.selected_agents.length}
      />

      <AnimatePresence>
        {error && (
          <motion.div className="boardroom-page__error" {...fadeSlide} key="error">
            <p>{error}</p>
            <button onClick={() => setStage("idle")} className="boardroom-page__retry">
              Try Again
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {mcpData && (
        <motion.div className="boardroom-page__mcp-info" {...fadeSlide}>
          <span className="boardroom-page__mcp-label">External Data:</span>
          <span className="boardroom-page__mcp-file">{mcpData.filename}</span>
          <span className="boardroom-page__mcp-size">
            ({(mcpData.file_size_bytes / 1024).toFixed(1)} KB)
          </span>
          {mcpData.total_rows && (
            <span className="boardroom-page__mcp-rows">{mcpData.total_rows} rows</span>
          )}
        </motion.div>
      )}

      <AnimatePresence>
        {orchestrationResult && (
          <motion.div className="boardroom-page__section" {...fadeSlide} key="depts">
            <h3 className="boardroom-page__section-title">Department Analyses</h3>
            <div className="boardroom-page__departments">
              {orchestrationResult.responses.map((result, idx) => (
                <motion.div
                  key={result.agent_id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2, delay: idx * 0.04 }}
                >
                  <DepartmentCard result={result} />
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {orchestrationResult && (
        <motion.div {...fadeSlide}>
          <ExecutionTimeline
            results={orchestrationResult.responses}
            totalTimeMs={orchestrationResult.execution_summary.total_execution_time_ms}
          />
        </motion.div>
      )}

      <AnimatePresence>
        {consensus && (
          <motion.div className="boardroom-page__section" {...fadeSlide} key="consensus">
            <ConsensusCard consensus={consensus} />
          </motion.div>
        )}
      </AnimatePresence>

      {consensus && orchestrationResult && (
        <motion.div {...fadeSlide}>
          <ConsensusCharts consensus={consensus} results={orchestrationResult.responses} />
        </motion.div>
      )}

      {consensus && (
        <motion.div className="boardroom-page__section" {...fadeSlide}>
          <h3 className="boardroom-page__section-title">Executive Summary</h3>
          <ExecutiveSummary consensus={consensus} />
        </motion.div>
      )}

      {consensus && orchestrationResult && (
        <motion.div className="boardroom-page__report-actions" {...fadeSlide}>
          <a
            className="boardroom-page__download-btn"
            href={`http://localhost:8000/api/reports/${orchestrationResult.session_id}?format=pdf`}
            target="_blank"
            rel="noopener noreferrer"
          >
            Download Executive Report (PDF)
          </a>
          <a
            className="boardroom-page__download-btn boardroom-page__download-btn--secondary"
            href={`http://localhost:8000/api/reports/${orchestrationResult.session_id}?format=json`}
            target="_blank"
            rel="noopener noreferrer"
          >
            View JSON Report
          </a>
        </motion.div>
      )}
    </div>
  );
}

export default BoardroomPage;
