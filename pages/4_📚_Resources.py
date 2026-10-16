import streamlit as st

st.set_page_config(page_title="Resources · SchistoScan", page_icon="📚", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%); }
h1 { color: #0e7490 !important; }
h2, h3 { color: #155e75 !important; }
section[data-testid="stSidebar"] { background-color: #ecfeff; }
</style>
""", unsafe_allow_html=True)

st.title("📚 Resources")
st.caption("Datasets, papers, and clinical references.")

st.header("Datasets")
st.markdown("""
| Dataset | Description |
|---|---|
| **STH_and_SM_Dataset_v1_0** | 10,562 microscopy images, 4 species |
| **Chula Parasite Egg Dataset** | Alternative parasite dataset |
| **NIH Schistosoma Image Database** | Historic microscopy |
""")

st.header("Peer-reviewed literature")
st.markdown("""
- Alzubaidi, L. et al. (2024). *Deep learning for intestinal parasite detection.*
- Kumar, S. et al. (2023). *Automated Schistosoma egg detection using YOLO.*
- Colley, D. G. et al. (2014). *Human schistosomiasis.* The Lancet.
- WHO (2023). *Schistosomiasis fact sheet.*
""")

st.header("Clinical standards")
st.markdown("""
- **Kato-Katz technique:** Standard stool smear for *S. mansoni*.
- **Urine filtration:** Standard for *S. haematobium*.
- **Treatment:** Praziquantel — WHO first-line.
""")

st.header("Tools used")
st.markdown("""
Ultralytics YOLO11 · PyTorch · Streamlit · OpenCV · Python 3.11
""")
