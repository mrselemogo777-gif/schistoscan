import streamlit as st

st.set_page_config(
    page_title="Contact · SchistoScan",
    page_icon="📬",
    layout="wide",
)

st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%); }
h1 { color: #0e7490 !important; }
h2, h3 { color: #155e75 !important; }
section[data-testid="stSidebar"] { background-color: #ecfeff; }
.stButton > button {
    background-color: #0e7490;
    color: white;
    border-radius: 6px;
    border: none;
    font-weight: 600;
}
.stButton > button:hover { background-color: #155e75; }
</style>
""", unsafe_allow_html=True)

st.title("📬 Contact")
st.caption("Questions, feedback, or collaboration on SchistoScan.")

# AUTHOR 
st.header("Author")

st.markdown("""
**Legakwa Selemogo**

Independent ML researcher · Botswana

Building decision-support tools for health and climate in Africa.
""")

#  MESSAGE FORM 
st.header("Send a message")

with st.form("contact_form", clear_on_submit=True):
    name    = st.text_input("Your name", placeholder="Jane Doe")
    email   = st.text_input("Your email", placeholder="jane@example.org")
    org     = st.text_input(
        "Organisation (optional)",
        placeholder="University / NGO / Clinic / Government",
    )
    topic   = st.selectbox("Topic", [
        "General question",
        "Clinical feedback",
        "Data / methodology",
        "Collaboration proposal",
        "Bug report",
        "Feature request",
        "Media / press",
    ])
    message = st.text_area(
        "Message",
        placeholder="Briefly describe your question or proposal...",
        height=150,
    )
    submitted = st.form_submit_button("📨 Send message")

    if submitted:
        if not name or not email or not message:
            st.error("Please fill in name, email, and message.")
        else:
            st.success(
                f"Thanks, **{name}**. Your message about *{topic}* "
                f"has been received. For the fastest response, you can also "
                f"[open an issue on GitHub]"
                f"(https://github.com/mrselemogo777-gif/schistoscan/issues/new)."
            )

# COLLABORATION 
st.header("Collaboration")

st.markdown("""
I am open to:

- **Field validation** of this tool with microscopy labs in Botswana
- **Data partnerships** with parasitology or public health researchers
- **Methodology feedback** from clinical microbiologists
- **Deployment support** for rural clinics
""")

st.markdown("---")
st.caption("SchistoScan · MIT License · 2026")
