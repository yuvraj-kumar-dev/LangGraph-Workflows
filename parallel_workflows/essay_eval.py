from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
import operator

# Define schema for structured output from LLM

class evalSchema(BaseModel):

    eval: str = Field(description='A Detailed feedback for the essay')
    score: int = Field(description='Evaluation Score for the essay out of 10', ge=0, le=10)

# Load LLM

llm = ChatOllama(model='codellama:7b')
structLLM = llm.with_structured_output(evalSchema)

# Define State

class evalState(TypedDict):

    essay: str
    language_feedback: str
    clarity_feedback: str
    analysis_feedback: str
    final_feedback: str
    individual_scores: Annotated[list[int], operator.add]
    avg_score: float

# Define graph

graph = StateGraph(evalState)

# Define Functions

def language_feedback(state: evalState) -> evalSchema:

    essay = state['essay']
    prompt = f'Give a detailed feedback and score out of 10 for the given essay on the basis of language quality. \n {essay}'
    output = structLLM.invoke(prompt)
    return {'language_feedback': output.eval, 'individual_scores': [output.score]}

def clarity_feedback(state: evalState) -> evalSchema:

    essay = state['essay']
    prompt = f'Give a detailed feedback and score out of 10 for the given essay on the basis of clarity of thoughts. \n {essay}'
    output = structLLM.invoke(prompt)
    return {'clarity_feedback': output.eval, 'individual_scores': [output.score]}

def analysis_feedback(state: evalState) -> evalSchema:

    essay = state['essay']
    prompt = f'Analyse the essay and give a detailed feedback and score out of 10 for the given essay. \n {essay}'
    output = structLLM.invoke(prompt)
    return {'analysis_feedback': output.eval, 'individual_scores': [output.score]}

def final_feedback(state: evalState) -> evalSchema:

    prompt = f'''Based on the following feedback, give a final summarised feedback \n 
    language feedback: {state['language_feedback']}, clarity feedback: {state['clarity_feedback']}, 
    analysis feedback: {state['analysis_feedback']}'''
    final_feedback = llm.invoke(prompt)

    avg_score = sum(state['individual_scores'])/len(state['individual_scores'])

    return {'final_feedback': final_feedback, 'avg_score': avg_score}


# Define nodes

graph.add_node('language_feedback', language_feedback)
graph.add_node('clarity_feedback', clarity_feedback)
graph.add_node('analysis_feedback', analysis_feedback)
graph.add_node('final_feedback', final_feedback)

# Define Edges

graph.add_edge(START, 'language_feedback')
graph.add_edge(START, 'clarity_feedback')
graph.add_edge(START, 'analysis_feedback')
graph.add_edge('language_feedback', 'final_feedback')
graph.add_edge('clarity_feedback', 'final_feedback')
graph.add_edge('analysis_feedback', 'final_feedback')
graph.add_edge('final_feedback', END)

# Compile

workflow = graph.compile()

# Invoke

essay = """ 

Rise of AI-Generated Content on Social Media: Understanding its Impact and Ethical Considerations

Introduction

Artificial intelligence (AI) has revolutionized numerous industries, but it is only recently that we have 
started to see its impact on social media. With the rise of AI-generated content, social media platforms are 
not just providing users with curated feeds of information, but also creating and consuming more automated content. 
This blog post aims to explore the rise of AI-generated content in social media, its impact on user engagement, 
brand reputation, and journalism, as well as the ethical considerations surrounding its use.

The Impact of AI-Generated Content on Social Media Platforms

AI-generated content is changing the way users interact with social media platforms. 
With algorithms prioritizing certain types of content over others, it is difficult for users to engage with 
a variety of perspectives and ideas. This can lead to a lack of diversity in content consumption and user 
engagement. Moreover, AI-generated content can have a negative impact on brand reputation and customer loyalty.    

The Role of Algorithms in Promoting AI-Generated Content

Algorithms play a significant role in promoting AI-generated content on social media platforms. 
They prioritize certain types of content over others based on factors such as engagement, relevance, 
and credibility. This can lead to a lack of diversity in content consumption and user engagement. 
Moreover, algorithms can manipulate or deceive users by prioritizing certain content that aligns with 
their pre-existing beliefs, leading to a loss of nuance and complexity in the information presented.

The Rise of Influencer Culture and AI-Generated Content

Influencer culture has become an essential part of social media, but it is also contributing to the rise of 
AI-generated content. Influencers are often encouraged to use AI-generated content in their marketing strategies, 
which can lead to a lack of diversity and complexity in content consumption. Moreover, influencer culture 
has become increasingly problematic due to its potential for misinformation and manipulation.

The Impact of AI-Generated Content on Journalism and Media

AI is changing the way news is created, distributed, and consumed. With more automated content creation, 
there is a risk of fake news and disinformation. Moreover, algorithms are increasingly being used to manipulate 
public opinion and sway political discourse. This can lead to a lack of nuance and complexity in the information 
presented, which can have serious ethical implications.

The Ethical Considerations of AI-Generated Content

AI is changing the way we consume and interact with information, but it also raises important ethical 
considerations. There is a risk of privacy breaches and security issues due to the increasing amount of 
automated content creation. Moreover, algorithms can manipulate or deceive users by prioritizing certain 
content that aligns with their pre-existing beliefs, leading to a loss of nuance and complexity in the 
information presented.

Conclusion

The rise of AI-generated content in social media has significant implications for user engagement, brand 
reputation, and journalism. It is essential to understand the impact of these changes and to reflect on the 
ethical considerations surrounding their use. We must engage with this topic and contribute to the conversation 
around the rise of AI-generated content in social media. By doing so, we can ensure that the benefits of AI 
are used for the greater good andnot used to manipulate or deceive people.

"""

initial_state = {'essay': essay}
final_state = workflow.invoke(initial_state)

print(final_state)
