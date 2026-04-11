from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

# Define State

class quadState(TypedDict):
    a: int
    b: int
    c: int

    quad_eqn: str
    discriminant: int
    roots: str



# Define graph

graph = StateGraph(quadState)

# Define Functions

def quadratic_eqn(state: quadState) -> quadState:

    a,b,c = state['a'], state['b'], state['c']
    quad_eqn = f'{a}x2 + {b}x + {c}'
    return {'quad_eqn': quad_eqn}

def calculate_disc(state: quadState) -> quadState:

    a,b,c = state['a'], state['b'], state['c']
    disc = (b**2) - (4*a*c)
    return {'discriminant': disc}

def real_roots(state: quadState) -> quadState:

    a,b,c = state['a'], state['b'], state['c']
    root1 = (-b + (state['discriminant'])**0.5) / 2*a
    root2 = (-b - (state['discriminant'])**0.5) / 2*a
    roots = f'The two real roots are {root1} and {root2}'
    return {'roots': roots}

def equal_roots(state: quadState) -> quadState:

    a,b,c = state['a'], state['b'], state['c']
    root1 = (-b + (state['discriminant'])**0.5) / 2*a
    roots = f'There exists two equal roots i.e {root1}'
    return {'roots': roots}

def no_real_roots(state: quadState) -> quadState:

    roots = f'There are no real roots for this quadratic equation'
    return {'roots': roots}

def check_disc(state: quadState) -> Literal['real_roots', 'equal_roots', 'no_real_roots']:

    if state['discriminant'] > 0:
        return 'real_roots'
    
    elif state['discriminant'] == 0:
        return 'equal_roots'
    
    else: 
        return 'no_real_roots'


# Define nodes

graph.add_node('quadratic_eqn', quadratic_eqn)
graph.add_node('calculate_disc', calculate_disc)
graph.add_node('real_roots', real_roots)
graph.add_node('equal_roots', equal_roots)
graph.add_node('no_real_roots', no_real_roots)

# Define edges

graph.add_edge(START, 'quadratic_eqn')
graph.add_edge('quadratic_eqn', 'calculate_disc')
graph.add_conditional_edges('calculate_disc', check_disc)
graph.add_edge('real_roots', END)
graph.add_edge('equal_roots', END)
graph.add_edge('no_real_roots', END)

# Compile

workflow = graph.compile()

# Invoke

initial_state = {'a': 1, 'b': -4, 'c': 4}
final_state = workflow.invoke(initial_state)
print(final_state)