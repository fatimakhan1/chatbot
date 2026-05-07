import streamlit as st
import requests

st.set_page_config(page_title="Medical Case Chatbot", page_icon="🏥", layout="centered")
st.title("🏥 Medical Case Chatbot")
st.caption("Ask anything about the Ahmed Raza Khan case file")
st.divider()

WEBHOOK_URL = "https://fatimakhan1.app.n8n.cloud/webhook/848af134-a1dd-4d95-8267-05f1535aaf8b"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask a question about the patient..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching case file..."):
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json={"question": prompt},
                    timeout=30
                )
                answer = response.json().get("output", "No answer returned.")
            except Exception as e:
                answer = f"Error: {str(e)}"
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
