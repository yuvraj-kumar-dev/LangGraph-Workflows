from langchain_community.llms import Ollama 
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Load LLM

llm = Ollama(model='codellama:7b')

# Define State

class llm_state(TypedDict):
    
    title: str
    outline: str
    content: str

# Define graph

graph = StateGraph(llm_state)

# Define functions

def create_outline(state: llm_state) -> llm_state:

    title = state['title']
    prompt = f'Create a well structured Outline for a blog on the topic {title}'
    outline = llm.invoke(prompt)
    state['outline'] = outline

    return state

def create_content(state: llm_state) -> llm_state:

    outline = state['outline']
    title = state['title']
    prompt = f'Create a blog on the topic {title} using this outline: {outline}'
    content = llm.invoke(prompt)
    state['content'] = content

    return state

# Define nodes

graph.add_node('create_outline', create_outline)
graph.add_node('create_content', create_content)

# Define edges

graph.add_edge(START, 'create_outline')
graph.add_edge('create_outline', 'create_content')
graph.add_edge('create_content', END)

# Compile

workflow = graph.compile()

# Invoke

initial_state = {'title': 'Rise of AI generated content on social media'}
final_state = workflow.invoke(initial_state)

print(final_state['content'])

# Rise of AI-Generated Content on Social Media: Understanding its Impact and Ethical Considerations

# Introduction

# Artificial intelligence (AI) has revolutionized numerous industries, but it is only recently that we have 
# started to see its impact on social media. With the rise of AI-generated content, social media platforms are 
# not just providing users with curated feeds of information, but also creating and consuming more automated content. 
# This blog post aims to explore the rise of AI-generated content in social media, its impact on user engagement, 
# brand reputation, and journalism, as well as the ethical considerations surrounding its use.

# The Impact of AI-Generated Content on Social Media Platforms

# AI-generated content is changing the way users interact with social media platforms. 
# With algorithms prioritizing certain types of content over others, it is difficult for users to engage with 
# a variety of perspectives and ideas. This can lead to a lack of diversity in content consumption and user 
# engagement. Moreover, AI-generated content can have a negative impact on brand reputation and customer loyalty.    

# The Role of Algorithms in Promoting AI-Generated Content

# Algorithms play a significant role in promoting AI-generated content on social media platforms. 
# They prioritize certain types of content over others based on factors such as engagement, relevance, 
# and credibility. This can lead to a lack of diversity in content consumption and user engagement. 
# Moreover, algorithms can manipulate or deceive users by prioritizing certain content that aligns with 
# their pre-existing beliefs, leading to a loss of nuance and complexity in the information presented.

# The Rise of Influencer Culture and AI-Generated Content

# Influencer culture has become an essential part of social media, but it is also contributing to the rise of 
# AI-generated content. Influencers are often encouraged to use AI-generated content in their marketing strategies, 
# which can lead to a lack of diversity and complexity in content consumption. Moreover, influencer culture 
# has become increasingly problematic due to its potential for misinformation and manipulation.

# The Impact of AI-Generated Content on Journalism and Media

# AI is changing the way news is created, distributed, and consumed. With more automated content creation, 
# there is a risk of fake news and disinformation. Moreover, algorithms are increasingly being used to manipulate 
# public opinion and sway political discourse. This can lead to a lack of nuance and complexity in the information 
# presented, which can have serious ethical implications.

# The Ethical Considerations of AI-Generated Content

# AI is changing the way we consume and interact with information, but it also raises important ethical 
# considerations. There is a risk of privacy breaches and security issues due to the increasing amount of 
# automated content creation. Moreover, algorithms can manipulate or deceive users by prioritizing certain 
# content that aligns with their pre-existing beliefs, leading to a loss of nuance and complexity in the 
# information presented.

# Conclusion

# The rise of AI-generated content in social media has significant implications for user engagement, brand 
# reputation, and journalism. It is essential to understand the impact of these changes and to reflect on the 
# ethical considerations surrounding their use. We must engage with this topic and contribute to the conversation 
# around the rise of AI-generated content in social media. By doing so, we can ensure that the benefits of AI 
# are used for the greater good andnot used to manipulate or deceive people.