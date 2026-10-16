import streamlit as st

st.set_page_config(page_title="Model & Data · SchistoScan", page_icon="📊", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%); }
h1 { color: #0e7490 !important; }
h2, h3 { color: #155e75 !important; }
section[data-testid="stSidebar"] { background-color: #ecfeff; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Model & Data")
st.caption("Training methodology, validation results, and dataset details.")

st.header("Model")
st.markdown("""
**Architecture:** YOLO11n — a lightweight object detection model (2.59M parameters).

**Why YOLO?** Parasite eggs must be *localised* (drawn as boxes) rather than just classified.

**Training:** 50 epochs, batch 16, image size 640×640, AdamW optimizer.
""")

st.header("Dataset")
st.markdown("""
**Source:** STH_and_SM_Dataset_v1_0

| Metric | Value |
|---|---|
| Total images | 10,562 |
| Total annotated eggs | 21,117 |
| Train / Val | 8,449 / 2,113 |

| Code | Species | Annotations |
|---|---|---|
| ASC. | *Ascaris lumbricoides* | 8,446 |
| TRI. | *Trichuris trichiura* | 4,020 |
| HKW. | Hookworm | 4,729 |
| SCH. | *Schistosoma mansoni* | 3,922 |
""")

st.header("Validation")
st.markdown("""
The final model was validated on **2,113 held-out test images**
(4,280 annotated eggs) never seen during training or model selection.

**Full validation metrics** — including per-species precision, recall,
mAP50, and mAP50-95 — are reported on the **📈 Results & Metrics** page.
""")

st.header("⚠️ Scope")
st.warning("""
**Decision-support tool, not a diagnostic device.**

Any positive flag must be confirmed by a qualified microscopist.
""")
