"""Upload + detect + results view for the Bilharzia AI app."""
from pathlib import Path
import tempfile

import streamlit as st
from PIL import Image

from services.detector import EggDetector
from services.risk import InfectionClassifier


class UploadView:
    """Renders the main microscopy image analysis panel."""

    def __init__(self, detector: EggDetector, classifier: InfectionClassifier):
        self.detector   = detector
        self.classifier = classifier

    
    # Public
    def render(self) -> None:
        st.subheader("Upload a microscopy image")
        st.caption(
            "Supported: PNG, JPG. Use a stool or urine microscopy image "
            "containing one or more parasite eggs."
        )

        uploaded = st.file_uploader(
            "Choose an image", type=["png", "jpg", "jpeg"]
        )

        col1, col2 = st.columns([1, 3])
        with col1:
            conf_threshold = st.slider(
                "Detection confidence threshold", 0.10, 0.90, 0.25, 0.05
            )
        with col2:
            st.write("")
            st.caption(
                "Lower threshold = more sensitive (more false positives). "
                "Higher threshold = more specific (may miss eggs)."
            )

        if uploaded is None:
            st.info("Upload an image to start detection.")
            return

        # Save upload to a temp file (YOLO expects a path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        if st.button("🔬 Analyze image", type="primary"):
            self._run_and_render(tmp_path, conf_threshold)

    
    # Internal
    def _run_and_render(self, image_path: str, conf_threshold: float) -> None:
        with st.spinner("Running detection..."):
            result = self.detector.detect(image_path, conf_threshold=conf_threshold)

        infection = self.classifier.classify(result["detections"])
        emoji, label = InfectionClassifier.label(infection.tier)

        # Flag
        if infection.tier == "POSITIVE":
            st.error(f"{emoji} **{label}**")
        elif infection.tier == "SUSPECTED":
            st.warning(f"{emoji} **{label}**")
        else:
            st.success(f"{emoji} **{label}**")

        # Summary metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Total eggs detected", infection.total_eggs)
        c2.metric("Species found", len(infection.per_species))
        c3.metric("Max confidence", f"{infection.max_confidence:.1%}")

        # Species breakdown
        if infection.per_species:
            st.markdown("**Species breakdown**")
            for species, count in infection.per_species.items():
                st.write(f"- {species}: **{count}**")

            if infection.has_schistosoma:
                st.warning(
                    "⚠️ **S. mansoni detected** — this is the parasite that "
                    "causes intestinal schistosomiasis (bilharzia)."
                )

        # Annotated image
        st.markdown("**Annotated image**")
        st.image(result["annotated"], caption="Detections shown in red boxes")

        # Detection detail table
        if result["detections"]:
            with st.expander("📊 Detection detail"):
                for i, det in enumerate(result["detections"], 1):
                    st.write(
                        f"{i}. **{det['class_name']}** — "
                        f"confidence {det['confidence']:.1%}, "
                        f"bbox {[round(x, 1) for x in det['bbox']]}"
                    )

        # Disclaimer
        st.markdown("---")
        st.caption(
            "⚠️ **Decision-support tool.** This is not a diagnosis. "
            "Any positive flag must be confirmed by a qualified microscopist "
            "before treatment."
        )
