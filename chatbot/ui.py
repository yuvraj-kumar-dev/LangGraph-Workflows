import streamlit as st
from chatbot_v1 import workflow
from langchain_core.messages import HumanMessage
import uuid

# Utility functions

def generate_thread():
    thread = uuid.uuid4()
    return thread

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'thread' not in st.session_state:
    st.session_state.thread = generate_thread()

st.sidebar.title('Langbot')

st.sidebar.button('New Chat')

st.sidebar.header('My Conversations')

st.sidebar.text(st.session_state.thread)


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.text(message['content'])


CONFIG = {'configurable': {'thread_id': st.session_state.thread}}


user_input = st.chat_input('Type here...')

if user_input:

    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    with st.chat_message('assistant'):
        resp = st.write_stream(message_chunk.content for message_chunk, metadata in workflow.stream({'messages': [HumanMessage(content=user_input)]}, 
                               config=CONFIG, 
                               stream_mode='messages'))
            
        st.session_state.messages.append({'role': 'assistant', 'content': resp})
