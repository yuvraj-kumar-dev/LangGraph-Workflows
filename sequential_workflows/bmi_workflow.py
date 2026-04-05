from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Define State

class bmiState(TypedDict):

    weight: float
    height: float
    bmi: float
    category: str

# Define Functions

def bmi_calculator(state: bmiState) -> bmiState:
    
    weight = state['weight']
    height = state['height']
    bmi = weight / (height ** 2)

    state['bmi'] = round(bmi, 2)
    return state

def category(state: bmiState) -> bmiState:
    if state['bmi'] <= 18.5:
        state['category'] = 'under_weight'

    elif state['bmi'] < 25:
        state['category'] = 'normal'

    elif state['bmi'] < 30:
        state['category'] = 'over_weight'

    else:
        state['category'] = 'obese'

    return state

# Define Graph

graph = StateGraph(bmiState)

# Define nodes

graph.add_node('bmi_calculator', bmi_calculator)
graph.add_node('bmi_category', category)

# Define edges

graph.add_edge(START, 'bmi_calculator')
graph.add_edge('bmi_calculator', 'bmi_category')
graph.add_edge('bmi_category', END)

# Compile 

workflow = graph.compile()

# Invoke

initial_state = {'weight': 60.0, 'height': 1.5}
final_state = workflow.invoke(initial_state)

print(final_state)