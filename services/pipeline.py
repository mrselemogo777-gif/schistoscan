"""Clinical pipeline — orchestrates detection, classification, and reporting.

Wraps the full inference flow so the UI only needs to call one method.
"""
import tempfile
from pathlib import Path
from typing import Optional

from services.detector import EggDetector, SPECIES_NAMES
from services.risk import InfectionClassifier, InfectionResult
from services.report import ClinicalReport


class ClinicalPipeline:
    """End-to-end clinical assessment pipeline.

    Usage:
        pipeline = ClinicalPipeline()
        result = pipeline.run(image_path, conf_threshold=0.25)
        pdf_bytes = pipeline.build_report(result, patient_id, sample_type, method)
    """

    def __init__(self):
        self.detector   = EggDetector()
        self.classifier = InfectionClassifier()

    
    # Detection
    def run(self, image_path: str, conf_threshold: float = 0.25) -> dict:
        """Run detection + classification on one image.

        Returns a dict with:
            detections  — list of detections from the detector
            annotated   — the annotated image (numpy array)
            infection   — InfectionResult from the classifier
            tier_emoji  — emoji for the tier
            tier_label  — human-readable label
            summary     — species breakdown with full names
        """
        raw = self.detector.detect(image_path, conf_threshold=conf_threshold)
        infection = self.classifier.classify(raw["detections"])
        emoji, label = InfectionClassifier.label(infection.tier)

        # Build species summary with full names
        summary = {}
        for short, count in infection.per_species.items():
            full = next(
                (v for k, v in SPECIES_NAMES.items()
                 if v.startswith(short.split()[0])),
                short,
            )
            summary[full] = count

        return {
            "detections": raw["detections"],
            "annotated":  raw["annotated"],
            "infection":  infection,
            "tier_emoji": emoji,
            "tier_label": label,
            "summary":    summary,
            "species_short": infection.per_species,
        }

    
    # Reporting
    def build_report(
        self,
        result: dict,
        patient_id: str,
        sample_type: str,
        method: str,
    ) -> bytes:
        """Generate a PDF report from a pipeline result.

        Parameters
        ----------
        result : dict
            The output of `run()`.
        patient_id, sample_type, method : str
            Sample metadata for the report header.

        Returns
        -------
        bytes — the PDF file content ready for st.download_button.
        """
        report = ClinicalReport(patient_id, sample_type, method)
        return report.build(
            result["infection"],
            result["detections"],
            result["annotated"],
        )

    
    # Convenience
    @staticmethod
    def who_intensity_tier(infection: InfectionResult) -> Optional[tuple]:
        """Return (emoji, tier_text) based on egg count, or None if not applicable."""
        if not infection.has_schistosoma:
            return None
        count = infection.total_eggs
        if count < 100:
            return ("🟢", "Light infection")
        if count < 400:
            return ("🟡", "Moderate infection")
        return ("🔴", "Heavy infection")

    @staticmethod
    def recommended_actions(infection: InfectionResult) -> list:
        """Return the recommended action bullets for the tier."""
        if infection.tier == "POSITIVE":
            return [
                "Confirm the detection under a calibrated microscope.",
                "If confirmed, follow national schistosomiasis treatment guidelines.",
                "Report per Botswana MoH surveillance protocol.",
            ]
        if infection.tier == "SUSPECTED":
            return [
                "Re-image the sample with better focus and lighting.",
                "If the finding persists, re-run with a lower confidence threshold.",
                "Submit for manual microscopist review.",
            ]
        return [
            "No eggs detected above the confidence threshold.",
            "If clinical suspicion persists, repeat sampling on a different day.",
        ]
