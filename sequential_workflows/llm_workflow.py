from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_community.llms import Ollama


# Load LLM

llm = Ollama(model='codellama:7b')

# Define State

class llm_state(TypedDict):

    question: str
    answer: str

# Define functions

def llm_qa(state: llm_state) -> llm_state:

    question = state['question']

    prompt = f'Answer the following question {question}'

    answer = llm.invoke(prompt)

    state['answer'] = answer

    return state

# Create graph

graph = StateGraph(llm_state)

# Create Nodes

graph.add_node('llm_qa', llm_qa)

# Create edges

graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)

# Compile

workflow = graph.compile()

# Invoke 

initital_state = {'question': 'What is __init__.py file in a project'}

final_state = workflow.invoke(initital_state)

print(final_state['answer'])

# The `__init__.py` file is a special file in Python that serves as a initialization file for a package. 
# When a package is imported, Python looks for an `__init__.py` file in the package's 
#     directory and executes its contents if it exists. The purpose of the `__init__.py` file is to 
# define custom initialization behavior for the package.

# For example, you can use the `__init__.py` file to:

# 1. Define global variables that are used by other modules in the package.
# 2. Import other modules or packages that are required by the package.
# 3. Define functions or classes that are used by other modules in the package.
# 4. Define custom exception types that are specific to the package.
# 5. Define custom configuration settings for the package.

# By using the `__init__.py` file, you can define a single place where all the initialization logic
# for your package is contained, making it easier to manage and maintain the code. Additionally, it
# allows you to have a more organized and structured project with clear boundaries between different 
# modules and packages.