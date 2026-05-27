import streamlit as st
import requests
import uuid

st.set_page_config(
    page_title="Chatbot",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #333333;
}
[data-testid="stSidebar"] button {
    width: 100%;
    background-color: transparent;
    color: #ececec;
    border-radius: 8px;
    border: none;
    padding: 10px 12px;
    margin-bottom: 4px;
    font-size: 14px;
}
[data-testid="stSidebar"] button:hover {
    background-color: #4da6ff;
    color: white;
    border: 1px solid #4da6ff;
}
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]){
            background-color: #1a3a5c;
            border-radius: 12px;
            color: white;
            padding: 10px;
            }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]){
            background-color: #1e1e2e;
            border-radius: 12px;
            color: white;
            padding: 10px;
            }
[data-testid="stChatInput"] {
    background-color: #1e1e1e;
    border: 2px solid #1a3a5c;
    border-radius: 12px;
    color: white;
}
h1 {
    color: #4da6ff;
}
</style>
           """, unsafe_allow_html=True)

st.title("chatbot")

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "session_id" not in st.session_state:
    session_id = str(uuid.uuid4())
    st.session_state.session_id = session_id
    st.session_state.chats[session_id] = []


with st.sidebar:
    st.title("Chats")
    if st.button("New Chat"):
        session_id = str(uuid.uuid4())
        st.session_state.session_id = session_id
        st.session_state.chats[session_id] = []

    for chat_id, messages in st.session_state.chats.items():

        if len(messages) > 0:
            title = messages[0]["content"][:20]
        else:
            title = "New Chat"

        if st.button(title, key=chat_id):
            st.session_state.session_id = chat_id

messages = st.session_state.chats[st.session_state.session_id]

st.write("current chat")

for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


text = st.chat_input("type your message here")

if text:

    messages.append({
        "role": "user",
        "content": text
    })

    with st.chat_message("user"):
        st.write(f"{text}")

    data = {
        "message": text,
        "session_id": st.session_state.session_id
    }

    try:

        response = requests.post(
            "http://localhost:8000/chat",
            json=data
        )

        response_data = response.json()

        if "reply" in response_data:

            messages.append({
                "role": "assistant",
                "content": response_data["reply"]
            })

            with st.chat_message("assistant"):
                st.write(f"{response_data['reply']}")

        else:
            st.error(
                response_data.get(
                    "detail",
                    "Unknown error"
                )
            )

    except Exception as e:
        st.error(f"Error: {e}")