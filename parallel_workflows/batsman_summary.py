from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Define State

class stats(TypedDict):

    runs: int
    balls: int
    fours: int
    sixes: int

    strike_rate: float
    boundary_percentage: float
    boundary_per_ball: float

    summary: str


# Define Graph

graph = StateGraph(stats)

# Define Functions

def calculate_sr(state: stats) -> stats:

    runs = state['runs']
    balls = state['balls']

    sr = round((runs/balls) * 100, 2)

    return {'strike_rate': sr}

def calculate_bpb(state: stats) -> stats:

    balls = state['balls']
    fours = state['fours']
    sixes = state['sixes']

    bpb = round((fours + sixes) / balls, 2)

    return {'boundary_per_ball': bpb}

def calculate_bp(state: stats) -> stats:

    runs = state['runs']
    fours = state['fours']
    sixes = state['sixes']

    bp = round(((4*fours + 6*sixes) / runs) * 100, 2)

    return {'boundary_percentage': bp}

def summary(state: stats) -> stats:

    sr = state['strike_rate']
    bp = state['boundary_percentage']
    bpb = state['boundary_per_ball']

    summary = f'''
                Strike Rate: {sr}
                Boundary Percentage: {bp}
                Boundary per Ball: {bpb}    
    '''
    

    return {'summary': summary}


# Define nodes

graph.add_node('calculate_sr', calculate_sr)
graph.add_node('calculate_bpb', calculate_bpb)
graph.add_node('calculate_bp', calculate_bp)
graph.add_node('summary', summary)

# Define edges

graph.add_edge(START, 'calculate_sr')
graph.add_edge(START, 'calculate_bpb')
graph.add_edge(START, 'calculate_bp')
graph.add_edge('calculate_sr', 'summary')
graph.add_edge('calculate_bpb', 'summary')
graph.add_edge('calculate_bp', 'summary')
graph.add_edge('summary', END)

# Compile

workflow = graph.compile()

# Invoke 

initial_state = {'runs': 150, 'balls': 65, 'fours': 16, 'sixes': 8}
final_state = workflow.invoke(initial_state)

print(final_state['summary'])