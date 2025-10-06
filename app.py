import streamlit as st
import base64
from src.gmail_helper.gmail_service import login_and_get_reader
from src.email_responder import generate_email_response

# Initialize GmailReader
reader = login_and_get_reader()

st.title("Email Response Generator")

# Initialize session state
if "email_index" not in st.session_state:
    st.session_state.email_index = 0
if "email_list" not in st.session_state:
    st.session_state.email_list = reader.emails
if "email_cache" not in st.session_state:
    st.session_state.email_cache = []

# Helper function to get email body
def get_email_body(msg):
    payload = msg.get("payload", {})
    parts = payload.get("parts", [])
    body = ""
    if parts:
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data")
                if data:
                    body += base64.urlsafe_b64decode(data).decode("utf-8")
    else:
        data = payload.get("body", {}).get("data")
        if data:
            body += base64.urlsafe_b64decode(data).decode("utf-8")
    return body

# Ensure current email is cached
if len(st.session_state.email_cache) <= st.session_state.email_index:
    msg_id = st.session_state.email_list[st.session_state.email_index]["id"]
    msg = reader.service.users().messages().get(userId="me", id=msg_id, format="full").execute()
    st.session_state.email_cache.append(get_email_body(msg))

# Display email textarea
email_input = st.text_area(
    "Email Content",
    value=st.session_state.email_cache[st.session_state.email_index],
    height=200
)

# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Previous Email"):
        if st.session_state.email_index > 0:
            st.session_state.email_index -= 1

with col2:
    if st.button("Next Email"):
        if st.session_state.email_index + 1 < len(st.session_state.email_list):
            st.session_state.email_index += 1
            # Cache the next email if not already cached
            if len(st.session_state.email_cache) <= st.session_state.email_index:
                msg_id = st.session_state.email_list[st.session_state.email_index]["id"]
                msg = reader.service.users().messages().get(userId="me", id=msg_id, format="full").execute()
                st.session_state.email_cache.append(get_email_body(msg))

# Tone selection
tone = st.selectbox("Select Tone", ["friendly", "professional", "formal"])

# Generate reply button
if st.button("Generate Reply"):
    if email_input.strip():
        reply = generate_email_response(email_input, tone)
        st.text_area("Generated Reply", value=reply, height=200)
    else:
        st.warning("Email content is empty.")
