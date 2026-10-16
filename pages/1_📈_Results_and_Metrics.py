import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Results & Metrics · SchistoScan",
    page_icon="📈",
    layout="wide",
)

st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%); }
h1 { color: #0e7490 !important; }
h2, h3 { color: #155e75 !important; }
section[data-testid="stSidebar"] { background-color: #ecfeff; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Results & Metrics")
st.caption("Verified model performance on held-out test data.")

st.info(
    "All metrics reported on **2,113 test images** (4,280 annotated eggs) "
    "never seen during training or validation."
)

# Headline metrics 
st.header("Overall performance")

c1, c2, c3, c4 = st.columns(4)
c1.metric("mAP50", "0.973")
c2.metric("mAP50-95", "0.927")
c3.metric("Precision", "0.944")
c4.metric("Recall", "0.928")

st.markdown("---")

# Per-species table 
st.header("Per-species performance")

per_species = pd.DataFrame([
    {"Species": "Ascaris lumbricoides",     "Code": "ASC.", "Precision": 0.964, "Recall": 0.962, "mAP50": 0.984, "mAP50-95": 0.947},
    {"Species": "Trichuris trichiura",      "Code": "TRI.", "Precision": 0.963, "Recall": 0.952, "mAP50": 0.987, "mAP50-95": 0.946},
    {"Species": "Hookworm",                 "Code": "HKW.", "Precision": 0.906, "Recall": 0.917, "mAP50": 0.960, "mAP50-95": 0.925},
    {"Species": "Schistosoma mansoni",      "Code": "SCH.", "Precision": 0.945, "Recall": 0.881, "mAP50": 0.961, "mAP50-95": 0.890},
])
st.dataframe(per_species, use_container_width=True, hide_index=True)

st.markdown("---")

# Interpretation 
st.header("What these metrics mean")

st.markdown("""
**mAP50** — Mean Average Precision at IoU ≥ 0.50. This is the standard
object detection metric. A value of **0.973** means that, on average,
the model finds 97.3% of eggs with correct localisation and classification.

**mAP50-95** — Same but averaged across IoU thresholds 0.50 to 0.95.
Stricter. A value of **0.927** means the model performs well even when
requiring tighter bounding box precision.

**Precision** — Of all eggs the model flags, what fraction are real eggs?
0.944 → **94.4% of flags are correct**.

**Recall** — Of all eggs actually present, what fraction does the model
catch? 0.928 → **92.8% of eggs are found**.
""")

st.markdown("---")

#  S. mansoni focus 
st.header("S. mansoni focus (target species)")

st.markdown("""
*Schistosoma mansoni* causes intestinal schistosomiasis — the primary
target of this tool.

| Metric | Value |
|---|---|
| Precision | **0.945** |
| Recall | **0.881** |
| mAP50 | **0.961** |
| mAP50-95 | **0.890** |

**In clinical terms:** For every 100 *S. mansoni* eggs in a sample, the
model correctly identifies **88**. Of the eggs the model flags as
*S. mansoni*, **94.5%** are correct.
""")

st.markdown("---")

# Training summary 
st.header("Training summary")

st.markdown("""
| Parameter | Value |
|---|---|
| Architecture | YOLO11n |
| Parameters | 2.59 M |
| Epochs | 50 |
| Image size | 640 × 640 |
| Batch size | 16 |
| Optimizer | AdamW (auto) |
| Hardware | CPU (Intel Core i7-5600U) |
| Training time | 56.8 hours |
""")

st.markdown("---")
st.caption(
    "All metrics verified on held-out test data. "
    "See *Model & Data* page for methodology."
)
