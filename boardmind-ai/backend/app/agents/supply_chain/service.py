"""Supply Chain Agent service.

This module provides the SupplyChainAgentService which:
1. Receives a business proposal
2. Builds the Supply Chain prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns a SupplyChainAgentResponse object
"""

import json
import logging
from typing import Optional

from .prompt import SUPPLY_CHAIN_SYSTEM_PROMPT, build_supply_chain_prompt
from .schema import SupplyChainAgentRequest, SupplyChainAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


class SupplyChainAgentService:
    """Service for the Supply Chain Agent in Department Workspace mode.

    This class encapsulates the complete Supply Chain Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = SupplyChainAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: SupplyChainAgentRequest) -> SupplyChainAgentResponse:
        """Analyze a business proposal from the CSCO perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated SupplyChainAgentResponse with complete supply chain analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_supply_chain_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for Supply Chain Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="supply_chain",
            llm_generate=self.llm.generate,
            system_prompt=SUPPLY_CHAIN_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> SupplyChainAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated SupplyChainAgentResponse.

        Raises:
            ValueError: If parsing or validation fails.
        """
        # Strip markdown code fences if present
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM response is not valid JSON: {e}")

        # Ensure agent_id is correct
        data["agent_id"] = "supply_chain"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return SupplyChainAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: SupplyChainAgentRequest) -> SupplyChainAgentResponse:
        """Generate a realistic mock response for development and testing.

        This mock demonstrates the expected output quality and structure
        without requiring an LLM. It analyzes keywords in the scenario
        to produce a contextually relevant response.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "supply_chain")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["diversify", "reshore", "optimize", "consolidate"]):
            position = "support"
            confidence = 0.75
        elif any(word in scenario_lower for word in ["single source", "rush", "untested", "unknown vendor"]):
            position = "oppose"
            confidence = 0.7
        elif any(word in scenario_lower for word in ["expand", "new market", "scale", "international"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine operational risk
        if any(word in scenario_lower for word in ["single supplier", "geopolitical", "critical component", "sole source"]):
            operational_risk = "critical"
        elif any(word in scenario_lower for word in ["international", "cross-border", "new region", "complex"]):
            operational_risk = "high"
        elif any(word in scenario_lower for word in ["local", "established", "proven"]):
            operational_risk = "low"
        else:
            operational_risk = "medium"

        return SupplyChainAgentResponse(
            agent_id="supply_chain",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "supply_chain_impact": (
                    "This initiative introduces moderate-to-significant changes in supply "
                    "chain operations. Current throughput capacity requires assessment for "
                    "handling increased volume or new product categories. Lead times may "
                    "shift by 2-4 weeks during transition period before stabilizing."
                ),
                "vendor_dependency": (
                    "Current supplier concentration presents moderate risk. Primary suppliers "
                    "handle 60-70% of volume with limited backup options. Recommendation: "
                    "qualify 2-3 alternative suppliers before commitment to reduce single-point "
                    "failure risk in critical supply paths."
                ),
                "logistics_complexity": (
                    "Distribution network changes are moderate in complexity. Existing "
                    "infrastructure can support initial phase, but scaling requires new "
                    "logistics partnerships or warehouse capacity. Cross-border elements "
                    "add customs, compliance, and transit time considerations."
                ),
                "procurement_needs": (
                    "Sourcing requirements include qualification of new suppliers (60-90 day "
                    "process), updated procurement contracts, and potential volume commitment "
                    "negotiations. Current procurement team capacity is adequate for initial "
                    "phase but may need augmentation for full-scale execution."
                ),
                "operational_risk": operational_risk,
            },
            summary=(
                f"From a supply chain perspective, this proposal is {position} with "
                f"{confidence:.0%} confidence — operational feasibility depends on "
                f"supplier qualification and logistics infrastructure readiness."
            ),
            rationale=(
                evidence_prefix +
                "From a supply chain operations standpoint, this initiative is feasible "
                "but requires careful sequencing to avoid disruption to existing operations. "
                "The current supply network has limited surge capacity, and any transition "
                "must be planned to maintain service levels during the changeover period.\n\n"
                "Vendor qualification is the critical path item. New suppliers require "
                "60-90 days minimum for qualification, including quality audits, capacity "
                "verification, and pilot production runs. Rushing this process to meet "
                "aggressive timelines creates quality and reliability risks that compound "
                "downstream through the supply chain.\n\n"
                "I recommend a phased approach: Phase 1 focuses on supplier qualification "
                "and logistics network design (90 days), Phase 2 on pilot operations at "
                "reduced volume (60 days), and Phase 3 on full-scale transition. This "
                "sequencing protects operational continuity while building the supply "
                "chain infrastructure needed for long-term success."
            ),
            risks=[
                "Supplier qualification timeline may extend beyond 90 days for specialized components — creates schedule dependency risk",
                "Logistics transition period (4-6 weeks) may result in delivery delays and increased backorder rates",
                "Vendor concentration risk if backup suppliers are not qualified before primary supplier relationship changes",
                "Demand forecasting accuracy decreases during transition, leading to inventory imbalances (overstock or stockouts)",
            ],
            conditions=[
                "Qualify minimum 2 alternative suppliers for critical components before committing to supply chain changes",
                "Maintain 30-day safety stock buffer during transition period to absorb delivery variability",
                "Complete logistics network assessment confirming capacity for 120% of projected peak volume",
                "Establish vendor performance SLAs with penalty clauses before transitioning volume to new suppliers",
            ],
            metrics_to_track=[
                "On-time delivery rate — maintain above 95% during transition, target 98% at steady state",
                "Supplier lead time variability — track weekly, alert if standard deviation exceeds 20% of mean",
                "Inventory turnover ratio — monitor for degradation during transition period",
                "Procurement cost per unit — track against baseline, alert if exceeds 10% increase",
                "Supply chain disruption events — count and classify, target zero critical disruptions",
            ],
            references_to=[],
        )
