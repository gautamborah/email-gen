# app.py
import sys
import streamlit as st

# Add the src folder to Python path
sys.path.append("src")

from email_responder import generate_email_response

st.set_page_config(page_title="AI Email Responder", page_icon="📧", layout="centered")

st.title("📧 AI Email Responder")
st.write("Paste an email below and let AI craft a professional response for you.")

# Email input box
email_input = st.text_area("✉️ Paste the received email:", height=250)

# Tone selector
tone = st.selectbox(
    "Select the tone of your reply:",
    ["friendly", "professional", "apologetic", "enthusiastic", "neutral"]
)

# Generate button
if st.button("Generate Reply"):
    if not email_input.strip():
        st.warning("Please paste an email first.")
    else:
        with st.spinner("Generating your reply..."):
            try:
                reply = generate_email_response(email_input, tone)
                st.subheader("📝 Suggested Reply")
                st.write(reply)
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Powered by LangChain + OpenAI • Built by Gautam 🚀")
