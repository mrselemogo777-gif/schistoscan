import streamlit as st

st.set_page_config(page_title="About · SchistoScan", page_icon="ℹ️", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%); }
h1 { color: #0e7490 !important; }
h2, h3 { color: #155e75 !important; }
section[data-testid="stSidebar"] { background-color: #ecfeff; }
</style>
""", unsafe_allow_html=True)

st.title("ℹ️ About SchistoScan")
st.caption("A decision-support tool for parasite egg detection")

st.header("⚠️ Scope")
st.warning("""
**Decision-support tool, not a diagnostic device.**

Flags parasite eggs in microscopy images for review by a qualified microscopist.
""")

st.header("Why Schistosomiasis?")
st.markdown("""
Schistosomiasis (bilharzia) is a neglected tropical disease affecting
~200 million people globally. In Botswana, intestinal schistosomiasis
caused by *Schistosoma mansoni* remains a public health concern.

Diagnosis requires detecting eggs in stool samples under a microscope.
Trained microscopists are scarce in rural clinics.
""")

st.header("What the tool does")
st.markdown("""
1. Accepts a microscopy image.
2. Runs YOLO11n to localise and classify every egg.
3. Displays the annotated image with red boxes.
4. Reports a three-tier flag:
   - 🔴 POSITIVE — high-confidence detection
   - 🟡 SUSPECTED — low-confidence, review manually
   - 🟢 NEGATIVE — no eggs detected
""")

st.header("What it does not do")
st.markdown("""
-  Does not diagnose
-  Does not prescribe treatment
-  Does not replace a microscopist
-  Does not work reliably on blurry images
""")

st.header("Author")
st.markdown("""
**Legakwa Selemogo** · [@mrselemogo777-gif](https://github.com/mrselemogo777-gif)

## License
MIT
""")
