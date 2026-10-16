"""Input form — patient info, sample type, method, image source."""
from pathlib import Path

import streamlit as st


class SampleInputForm:
    """Renders the sample information form + image source selector.

    Returns the collected inputs via `.result` after render().
    """

    def __init__(self):
        self.patient_id    = None
        self.sample_type   = None
        self.method        = None
        self.conf_threshold = None
        self.image_source  = None

    
    # Public
    def render(self) -> dict:
        """Draw the form. Returns the collected settings dict."""
        st.header("1. Sample information")

        c1, c2, c3 = st.columns(3)
        with c1:
            self.patient_id = st.text_input(
                "Patient ID (optional)",
                placeholder="ANON",
            )
        with c2:
            self.sample_type = st.selectbox(
                "Sample type",
                ["Stool", "Other"],
                help=(
                    "This model is validated on stool microscopy images only. "
                    "Urine microscopy requires S. haematobium detection, "
                    "which is not supported in this version."
                ),
            )
        with c3:
            self.method = st.selectbox(
                "Method",
                [
                    "Kato-Katz",
                    "Direct smear",
                    "Formol-ether concentration",
                    "Other",
                ],
                help=(
                    "Kato-Katz is the WHO-recommended method for S. mansoni "
                    "egg counting in stool."
                ),
            )

        st.header("2. Upload microscopy image")

        uploaded = st.file_uploader(
            "Choose an image", type=["png", "jpg", "jpeg"]
        )
        self._demo_selector()

        self.conf_threshold = st.slider(
            "Detection confidence threshold",
            0.10, 0.90, 0.25, 0.05,
            help="Lower = more sensitive. Higher = more specific.",
        )

        self._resolve_image_source(uploaded)

        return self._to_dict()

    
    # Internal
    def _demo_selector(self) -> None:
        st.markdown("**Or test with a demo sample:**")
        demo_cols = st.columns(4)

        demo_options = {
            "🟠 S. mansoni": "sch",
            "🟢 Ascaris":    "asc",
            "🔵 Trichuris":  "tri",
            "🟣 Hookworm":   "hkw",
        }

        for i, (label, folder) in enumerate(demo_options.items()):
            with demo_cols[i]:
                if st.button(label, key=f"demo_{folder}"):
                    demo_dir = Path("data/demo") / folder
                    files = (
                        sorted(demo_dir.glob("*.png"))
                        + sorted(demo_dir.glob("*.jpg"))
                    )
                    if files:
                        st.session_state["demo_image"] = str(files[0])
                        st.success(f"Loaded demo sample: {files[0].name}")

    def _resolve_image_source(self, uploaded) -> None:
        import tempfile
        if uploaded is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(uploaded.read())
                self.image_source = tmp.name
        elif "demo_image" in st.session_state:
            self.image_source = st.session_state["demo_image"]

    def _to_dict(self) -> dict:
        return {
            "patient_id":     self.patient_id,
            "sample_type":    self.sample_type,
            "method":         self.method,
            "conf_threshold": self.conf_threshold,
            "image_source":   self.image_source,
        }
