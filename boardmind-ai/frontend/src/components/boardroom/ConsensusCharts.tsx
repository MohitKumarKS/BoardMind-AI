import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { ConsensusResult, AgentExecutionResult } from "../../services/boardroomApi";
import "./Boardroom.css";

interface ConsensusChartsProps {
  consensus: ConsensusResult;
  results: AgentExecutionResult[];
}

const VOTE_COLORS = {
  Support: "#22c55e",
  Conditional: "#f59e0b",
  Neutral: "#6b7280",
  Oppose: "#ef4444",
};

const AGENT_COLORS: Record<string, string> = {
  finance: "#22c55e",
  marketing: "#a855f7",
  sales: "#3b82f6",
  hr: "#f97316",
  operations: "#6b7280",
  legal: "#ef4444",
  it: "#14b8a6",
  business_analytics: "#6366f1",
};

function ConsensusCharts({ consensus, results }: ConsensusChartsProps) {
  // Vote distribution pie
  const voteData = [
    { name: "Support", value: consensus.support_count },
    { name: "Conditional", value: consensus.conditional_count },
    { name: "Neutral", value: consensus.neutral_count },
    { name: "Oppose", value: consensus.oppose_count },
  ].filter((d) => d.value > 0);

  // Confidence bar chart
  const confidenceData = results
    .filter((r) => r.status === "completed" && r.response)
    .map((r) => ({
      name: (r.agent_id || "").replace("_", " ").slice(0, 8),
      confidence: Math.round(Number(r.response?.confidence || 0) * 100),
      fill: AGENT_COLORS[r.agent_id] || "#6b7280",
    }));

  // Execution time bar chart
  const timeData = results.map((r) => ({
    name: (r.agent_id || "").replace("_", " ").slice(0, 8),
    time: r.execution_time_ms,
    fill: AGENT_COLORS[r.agent_id] || "#6b7280",
  }));

  return (
    <div className="br-charts">
      <div className="br-charts__card">
        <h4 className="br-charts__title">Vote Distribution</h4>
        <ResponsiveContainer width="100%" height={180}>
          <PieChart>
            <Pie
              data={voteData}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={70}
              paddingAngle={3}
              dataKey="value"
            >
              {voteData.map((entry) => (
                <Cell key={entry.name} fill={VOTE_COLORS[entry.name as keyof typeof VOTE_COLORS]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ background: "#18181b", border: "1px solid #27272a", borderRadius: "8px", fontSize: "12px" }}
              labelStyle={{ color: "#fafafa" }}
              itemStyle={{ color: "#a1a1aa" }}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="br-charts__legend">
          {voteData.map((d) => (
            <span key={d.name} className="br-charts__legend-item">
              <span className="br-charts__legend-dot" style={{ background: VOTE_COLORS[d.name as keyof typeof VOTE_COLORS] }} />
              {d.name} ({d.value})
            </span>
          ))}
        </div>
      </div>

      <div className="br-charts__card">
        <h4 className="br-charts__title">Department Confidence</h4>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={confidenceData} layout="vertical" margin={{ left: 10, right: 10 }}>
            <XAxis type="number" domain={[0, 100]} hide />
            <YAxis type="category" dataKey="name" width={60} tick={{ fill: "#a1a1aa", fontSize: 10 }} />
            <Tooltip
              contentStyle={{ background: "#18181b", border: "1px solid #27272a", borderRadius: "8px", fontSize: "12px" }}
              formatter={(value) => [`${value}%`, "Confidence"]}
            />
            <Bar dataKey="confidence" radius={[0, 4, 4, 0]} barSize={14}>
              {confidenceData.map((entry, idx) => (
                <Cell key={idx} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {timeData.some((d) => d.time > 0) && (
        <div className="br-charts__card">
          <h4 className="br-charts__title">Execution Time (ms)</h4>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={timeData} layout="vertical" margin={{ left: 10, right: 10 }}>
              <XAxis type="number" hide />
              <YAxis type="category" dataKey="name" width={60} tick={{ fill: "#a1a1aa", fontSize: 10 }} />
              <Tooltip
                contentStyle={{ background: "#18181b", border: "1px solid #27272a", borderRadius: "8px", fontSize: "12px" }}
                formatter={(value) => [`${value}ms`, "Time"]}
              />
              <Bar dataKey="time" radius={[0, 4, 4, 0]} barSize={14}>
                {timeData.map((entry, idx) => (
                  <Cell key={idx} fill={entry.fill} opacity={0.7} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default ConsensusCharts;
