import streamlit as st
import requests
import uuid

st.set_page_config(
    page_title = "Chatbot",
    layout = "wide"
)

st.title("chatbot")

with st.sidebar:
  st.title("chats")
  if st.button("chat"):
   st.session_state.messages = []
   st.session_state.session_id = str(uuid.uuid4())


st.write("current chat")



if "session_id" not in  st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**you**: {msg['content']}")
    else:
        st.markdown(f"**bot**: {msg['content']}")

text = st.chat_input("type your message here")

if text:
    st.session_state.messages.append(
        {"role": "user",
         "content" : text}
    )

    with st.chat_message("user"):
     st.markdown(text)

    payload = {
    "message" : text,
    "session_id" : st.session_state.session_id
    }

    try :
       response = requests.post("http://localhost:8000/chat", json=payload)
       response_data = response.json()
       st.write(response_data)

       if "reply" in response_data:

         st.session_state.messages.append(
          {
            "role": "assistant",
            "content": response_data["reply"]
          }
         )

         with st.chat_message("assistant"):
          st.markdown(response_data["reply"])

       else:
         st.error(response_data.get("detail", "Unknown error"))


    except Exception as e:
      st.error(f"Error: {e}")