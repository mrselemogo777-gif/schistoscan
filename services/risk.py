"""Map detections to an infection risk tier.

Three tiers:
    POSITIVE  — at least one egg detected with confidence >= 0.5
    SUSPECTED — eggs detected, but highest confidence is 0.25–0.5
    NEGATIVE  — no eggs detected above the detection threshold
"""
from dataclasses import dataclass, field
from typing import List, Dict


POSITIVE_CONF  = 0.50   # above this → positive
SUSPECTED_CONF = 0.25   # above this → suspected


@dataclass
class InfectionResult:
    """Decision output for one image."""
    tier: str                             # "POSITIVE" | "SUSPECTED" | "NEGATIVE"
    total_eggs: int
    per_species: Dict[str, int] = field(default_factory=dict)
    max_confidence: float = 0.0
    has_schistosoma: bool = False         # S. mansoni specifically detected
    species_names: List[str] = field(default_factory=list)


class InfectionClassifier:
    """Convert a detection list into a tiered infection flag."""

    def __init__(self, positive_conf: float = POSITIVE_CONF,
                 suspected_conf: float = SUSPECTED_CONF):
        self.positive_conf  = positive_conf
        self.suspected_conf = suspected_conf

    
    def classify(self, detections: List[Dict]) -> InfectionResult:
        """Run the tier logic on a list of detections."""
        if not detections:
            return InfectionResult(tier="NEGATIVE", total_eggs=0)

        per_species = {}
        max_conf    = 0.0
        has_sch     = False

        for d in detections:
            species = d["short_name"]
            per_species[species] = per_species.get(species, 0) + 1

            conf = d["confidence"]
            if conf > max_conf:
                max_conf = conf

            if d["class_code"] == "SCH.":
                has_sch = True

        # Decide tier
        if max_conf >= self.positive_conf:
            tier = "POSITIVE"
        elif max_conf >= self.suspected_conf:
            tier = "SUSPECTED"
        else:
            tier = "NEGATIVE"

        return InfectionResult(
            tier=tier,
            total_eggs=len(detections),
            per_species=per_species,
            max_confidence=max_conf,
            has_schistosoma=has_sch,
            species_names=list(per_species.keys()),
        )

    
    @staticmethod
    def label(tier: str) -> tuple:
        """Return (emoji, text) for the tier."""
        return {
            "POSITIVE":  ("🔴", "POSITIVE — Eggs detected at high confidence"),
            "SUSPECTED": ("🟡", "SUSPECTED — Low-confidence detections, review manually"),
            "NEGATIVE":  ("🟢", "NEGATIVE — No eggs detected above threshold"),
        }[tier]
