from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
import operator

# Load LLM

generator_llm = ChatOllama(model='phi4-mini:3.8b')
eval_llm = ChatOllama(model='phi4-mini:3.8b')
optimizer_llm = ChatOllama(model='phi4-mini:3.8b')

class eval(BaseModel):

    eval: Literal['approve', 'reject'] = Field(description='You are a post evaluator, evaluate this post and approve or reject this post')
    feedback: str = Field(description='Evaluate this post and provide a detail feedback for it')

evaluator_llm = eval_llm.with_structured_output(eval)

# Define state

class postState(TypedDict):

    topic: str
    post: str
    eval: Literal['approve', 'reject']
    feedback: str
    iteration: int
    max_iteration: int

    feedbacks: Annotated[list[str], operator.add]
    posts: Annotated[list[str], operator.add]

# Define Graph

graph = StateGraph(postState)

# Define Functions

def generate(state: postState) -> postState:

    topic = state['topic']
    prompt = f"""

        You are an expert content creator for X (Twitter).

        Topic: {topic}

        Your task:
        - Write a highly engaging X post
        - Keep it concise (max 280 characters)
        - Make it informative, interesting, and shareable
        - Use a strong hook in the first line
        - Use simple and clear language
        - Add emojis only if they improve engagement
        - Avoid fluff

        Return STRICT JSON:

        {{
        "post": "Your final X post here"
        }}

        DO NOT return anything except JSON.

    """

    resp = generator_llm.invoke(prompt).content
    return {'post': resp, 'posts': [resp]}

def evaluate(state: postState) -> postState:
    topic = state['topic']
    prompt = f"""

        You are a senior social media strategist.

        Topic: {topic}

        Evaluate the following X post and also give a feedback:

        POST:
        {{post}}

        Evaluation criteria:
        - Clarity (easy to understand)
        - Engagement (hook, curiosity, shareability)
        - Relevance to topic
        - Conciseness
        - Originality

        Rules:
        - score >= 8 → approve
        - score < 8 → reject
        - Be critical and honest

        ONLY return JSON.

    """

    resp = evaluator_llm.invoke(prompt)
    return {'eval': resp.eval, 'feedback': resp.feedback, 'feedbacks': [resp.feedback]}

def optimize(state: postState) -> postState:
    topic = state['topic']
    feedback = state['feedback']
    iteration = state['iteration']
    prompt = f"""

            You are an expert X (Twitter) content optimizer.

            Topic: {topic}

            Previous post feedback:
            {feedback}

            Your task:
            - Improve the X post based on feedback
            - Fix all weaknesses mentioned
            - Make it more engaging and clearer
            - Keep it under 280 characters

            Return STRICT JSON:

            {{
            "post": "Improved X post"
            }}

            ONLY return JSON.

    """

    resp = optimizer_llm.invoke(prompt).content
    return {'post': resp, 'posts': [resp], 'iteration': (iteration+1)}

def route(state: postState) -> Literal['approve', 'reject']:

    if state['eval'] == 'approve' or state['max_iteration'] == state['iteration']:
        return 'approve'
    else:
        return 'reject'

# Define nodes

graph.add_node('generate', generate)
graph.add_node('evaluate', evaluate)
graph.add_node('optimize', optimize)

# Define edges

graph.add_edge(START, 'generate')
graph.add_edge('generate', 'evaluate')
graph.add_conditional_edges('evaluate', route, {'approve': END, 'reject': 'optimize'})
graph.add_edge('optimize', 'evaluate')

# Compile 

workflow = graph.compile()

# Invoke

initial_state = {'topic': 'Use of AI in teens', 'max_iteration': 5, 'iteration': 1}
final_state = workflow.invoke(initial_state)

print(f"""posts: {final_state['posts']}

          feedbacks: {final_state['feedbacks']}

          iterations: {final_state['iteration']}

          max_iterations: {final_state['max_iteration']}           
      """)


