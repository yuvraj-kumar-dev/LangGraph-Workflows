import streamlit as st
from chatbot_v1 import workflow
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 1}}

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here...')

if user_input:

    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    with st.chat_message('assistant'):
        resp = workflow.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
        st.session_state.messages.append({'role': 'assistant', 'content': resp['messages'][-1].content})
        st.text(resp['messages'][-1].content)

