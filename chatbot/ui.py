import streamlit as st
from chatbot_v1 import workflow, retrieve_threads
from langchain_core.messages import HumanMessage
import uuid

# Utility functions

def generate_thread():
    thread = uuid.uuid4()
    return thread

def reset_chat():
    thread_id = generate_thread()
    st.session_state.thread = thread_id
    add_thread(st.session_state.thread)
    st.session_state.messages = []

def add_thread(thread_id):
    if thread_id not in st.session_state.chat_threads:
        st.session_state.chat_threads.append(thread_id)

def load_conversation(thread_id):
    return workflow.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'thread' not in st.session_state:
    st.session_state.thread = generate_thread()

if 'chat_threads' not in st.session_state:
    st.session_state.chat_threads = retrieve_threads()

add_thread(st.session_state.thread)

st.sidebar.title('Langbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state.chat_threads[::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state.thread = thread_id
        messages = load_conversation(thread_id)


        temp_msg = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_msg.append({'role': role, 'content': msg.content})

        st.session_state.messages = temp_msg


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
