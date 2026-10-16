"""Result view — renders the clinical assessment output."""
from datetime import datetime

import streamlit as st

from services.pipeline import ClinicalPipeline


class ResultView:
    """Renders detection result, metrics, and PDF download."""

    def __init__(self, pipeline: ClinicalPipeline):
        self.pipeline = pipeline

    
    # Public
    def render(self, result: dict, patient_id: str,
               sample_type: str, method: str) -> None:
        """Draw the full result panel."""
        infection = result["infection"]

        st.markdown("---")
        st.header("3. Result")

        self._render_flag(result)
        self._render_metrics(infection)
        self._render_who_tier(infection)
        self._render_species(result["summary"])
        self._render_image(result["annotated"])
        self._render_actions(infection)
        self._render_report_download(result, patient_id, sample_type, method)
        self._render_detection_detail(result["detections"])

    
    # Sub-renderers
    def _render_flag(self, result: dict) -> None:
        emoji = result["tier_emoji"]
        label = result["tier_label"]
        tier  = result["infection"].tier

        if tier == "POSITIVE":
            st.error(f"{emoji} **{label}**")
        elif tier == "SUSPECTED":
            st.warning(f"{emoji} **{label}**")
        else:
            st.success(f"{emoji} **{label}**")

    def _render_metrics(self, infection) -> None:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total eggs", infection.total_eggs)
        m2.metric("Species", len(infection.per_species))
        m3.metric("Max confidence", f"{infection.max_confidence:.1%}")
        m4.metric(
            "S. mansoni",
            "Detected" if infection.has_schistosoma else "Not detected",
        )

    def _render_who_tier(self, infection) -> None:
        st.subheader("Intensity interpretation (WHO)")
        tier = ClinicalPipeline.who_intensity_tier(infection)

        if tier is None:
            st.info(
                "No *S. mansoni* eggs detected. Intensity classification "
                "not applicable to intestinal schistosomiasis."
            )
            return

        emoji, text = tier
        st.markdown(f"{emoji} **{text}** — {infection.total_eggs} egg(s) in image.")
        st.caption(
            "*Note: WHO tiers use eggs per gram (EPG) of stool, not eggs "
            "per image. This estimate is a proxy only.*"
        )

    def _render_species(self, summary: dict) -> None:
        st.subheader("Species breakdown")
        if not summary:
            st.write("No eggs detected above the confidence threshold.")
            return
        for species, count in summary.items():
            st.markdown(f"- **{species}** — {count} egg(s)")

    def _render_image(self, annotated) -> None:
        st.subheader("Annotated image")
        st.image(annotated, caption="Detections shown in boxes")

    def _render_actions(self, infection) -> None:
        st.subheader("Recommended action")
        for line in ClinicalPipeline.recommended_actions(infection):
            st.markdown(f"- {line}")

    def _render_report_download(self, result: dict, patient_id: str,
                                sample_type: str, method: str) -> None:
        st.markdown("---")
        st.subheader("📄 Download clinical report")

        pdf_bytes = self.pipeline.build_report(
            result, patient_id, sample_type, method
        )

        fname = (
            f"schistoscan_report_"
            f"{patient_id or 'anon'}_"
            f"{datetime.utcnow().strftime('%Y%m%d_%H%M')}.pdf"
        )

        st.download_button(
            label="📄 Download PDF report",
            data=pdf_bytes,
            file_name=fname,
            mime="application/pdf",
        )
        st.caption(
            "The PDF report includes sample metadata, detection result, "
            "species breakdown, annotated image, and recommended action."
        )

    def _render_detection_detail(self, detections: list) -> None:
        with st.expander("📊 Full detection detail"):
            if not detections:
                st.write("No detections.")
                return
            for i, det in enumerate(detections, 1):
                st.write(
                    f"{i}. **{det['class_name']}** — "
                    f"confidence {det['confidence']:.1%} · "
                    f"bbox {[round(x, 1) for x in det['bbox']]}"
                )
