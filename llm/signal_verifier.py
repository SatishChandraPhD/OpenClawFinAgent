# llm/signal_verifier.py

from typing import Dict


class SignalVerifier:
    """
    Verification-aware reasoning layer.

    Goal:
    ensure cross-signal agreement before allowing strong actions.

    strengthens robustness and reduces drawdowns.
    """

    def __init__(
        self,
        agreement_threshold: float = 0.2,
        strong_signal_threshold: float = 1.0
    ):
        self.agreement_threshold = agreement_threshold
        self.strong_signal_threshold = strong_signal_threshold

    def verify(
        self,
        technical_score: float,
        llm_score: float,
        macro_score: float,
        combined_score: float
    ) -> Dict:

        agreement_strength = (
            abs(technical_score - llm_score) +
            abs(technical_score - macro_score)
        ) / 2

        disagreement_penalty = min(agreement_strength, 1.0)

        adjusted_score = combined_score * (1 - 0.25 * disagreement_penalty)

        reasoning = []

        if agreement_strength < self.agreement_threshold:
            reasoning.append("strong_cross_signal_agreement")

        if agreement_strength >= self.agreement_threshold:
            reasoning.append("signal_disagreement_penalty_applied")

        if abs(adjusted_score) >= self.strong_signal_threshold:
            reasoning.append("high_confidence_signal")

        return {

            "adjusted_score": adjusted_score,

            "agreement_strength": agreement_strength,

            "verification_confidence": 1 - disagreement_penalty,

            "reasoning": reasoning
        }