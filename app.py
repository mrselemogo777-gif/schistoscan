"""SchistoScan — Parasite egg detection from microscopy images.

Streamlit entry point. Wires together pipeline, form, result, and sidebar.
"""
import streamlit as st

from services.pipeline import ClinicalPipeline
from ui.input_form import SampleInputForm
from ui.result_view import ResultView
from ui.sidebar import ModelSidebar



# Page config
st.set_page_config(
    page_title="SchistoScan — Parasite Egg Detection",
    page_icon="🔬",
    layout="wide",
)



# Medical theme
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%); }
    h1 { color: #0e7490 !important; letter-spacing: -0.5px; }
    h2, h3 { color: #155e75 !important; }
    section[data-testid="stSidebar"] { background-color: #ecfeff; }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #0e7490 !important; }
    .stButton > button {
        background-color: #0e7490;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: 600;
    }
    .stButton > button:hover { background-color: #155e75; }
    div[data-testid="stAlert"] { border-radius: 8px; }
    div[data-testid="stMetricValue"] { color: #0e7490; font-weight: 700; }
    section[data-testid="stFileUploader"] {
        border: 2px dashed #0e7490;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# Header
col_logo, col_title = st.columns([1, 2])
with col_logo:
    st.image("assets/logo.png", use_container_width=True)
with col_title:
    st.title("🔬 SchistoScan")
    st.caption(
        "Parasite egg detection · Clinical decision-support · "
        "YOLO11n · 4 species · mAP50 = 0.973"
    )

st.warning(
    "**Decision-support tool, not a diagnosis.** All findings must be "
    "confirmed by a qualified microscopist before any treatment decision.",
    icon="⚠️",
)



# Bootstrap (cached)
@st.cache_resource(show_spinner=False)
def load_pipeline():
    return ClinicalPipeline()


pipeline = load_pipeline()



# Render
sidebar = ModelSidebar()
sidebar.render()

form = SampleInputForm()
inputs = form.render()

if inputs["image_source"] and st.button(
    "🧪 Run clinical assessment", type="primary"
):
    with st.spinner("Analyzing sample..."):
        result = pipeline.run(
            inputs["image_source"],
            conf_threshold=inputs["conf_threshold"],
        )

    view = ResultView(pipeline)
    view.render(
        result,
        patient_id=inputs["patient_id"],
        sample_type=inputs["sample_type"],
        method=inputs["method"],
    )



# Footer
st.markdown("---")
st.caption(
    "SchistoScan · YOLO11n · Decision-support tool — human review required · "
    "MIT License"
)
