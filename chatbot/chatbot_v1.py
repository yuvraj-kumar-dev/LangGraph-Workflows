from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Load LLM

llm = ChatOllama(model='phi4-mini:3.8b')

# Define State

class chatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]

# Define Graph

graph = StateGraph(chatState)

# Define Functions

def chatbot(state: chatState) -> chatState:

    user_message = state['messages']

    resp = llm.invoke(user_message)

    return {'messages': [resp]}

# Define nodes

graph.add_node('chatbot', chatbot)

# Define edges

graph.add_edge(START, 'chatbot')
graph.add_edge('chatbot', END)

# Compile

thread = 1 
memory = MemorySaver()

workflow = graph.compile(checkpointer=memory)

# Chatbot Invoke

if __name__ == '__main__':


    while True:

        config = {'configurable': {'thread_id': thread}}

        user_resp = input('Enter a message: ')
        print(f'User: {user_resp}')

        if user_resp.strip().lower() in ['exit', 'quit']:
            break

        resp = workflow.invoke({'messages': [HumanMessage(content=user_resp)]}, config=config)
        print(f"AI: {resp['messages'][-1].content}")


