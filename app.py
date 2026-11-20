import asyncio
import streamlit as st
from src.literary_agent.workflow import recommend

st.set_page_config(page_title="Literary Agent", page_icon="📚", layout="wide")
st.title("📚 Literary Agent")
st.caption("Describe what you want to read. Get five ranked, researched book recommendations.")

with st.form("request"):
    inquiry = st.text_area("What are you looking for?",
        placeholder="Example: I want to understand behavioral economics from beginner to advanced, with practical examples.",
        height=140)
    a, b = st.columns(2)
    with a:
        level = st.selectbox("Reading level", ["Any", "Beginner", "Intermediate", "Advanced", "Academic / Research"])
        language = st.selectbox("Preferred language", ["Any", "English", "Hindi", "Urdu", "Other"])
    with b:
        length = st.selectbox("Preferred length", ["Any", "Short (<200 pages)", "Medium (200–400 pages)", "Long (400+ pages)"])
        exclusions = st.text_input("Books already read / exclusions")
    submit = st.form_submit_button("Recommend my top 5", type="primary")

if submit:
    if not inquiry.strip():
        st.error("Please describe what you want to read.")
    else:
        with st.spinner("Analyzing your inquiry and searching book catalogs..."):
            try:
                st.session_state["result"] = asyncio.run(recommend(inquiry, level, language, length, exclusions))
            except Exception as e:
                st.error(f"{type(e).__name__}: {e}")

if st.session_state.get("result"):
    st.divider()
    st.markdown(st.session_state["result"])
    st.download_button("Download recommendations", st.session_state["result"],
        file_name="top_5_book_recommendations.md", mime="text/markdown")
