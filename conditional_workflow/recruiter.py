from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Literal, Annotated
from pydantic import BaseModel, Field
import operator

# Load LLM

llm = ChatOllama(model='phi4-mini:3.8b')

# Structure LLM response

class LLMstruct(BaseModel):

    eval: str = Field(description='Give a detailed feedback as an expert Recruiter on the basis of conversation with the candidate')
    score: int = Field(description='Give an Evaluation Score out of 10', ge=0, le=10)

llmstruct = llm.with_structured_output(LLMstruct)

# Define State

class recruitState(TypedDict):

    ans1: str
    ans2: str
    ans3: str

    techEval: str
    commEval: str
    probSolvingEval: str
    redFlagEval: str
    summary: str

    individualScores: Annotated[list[int], operator.add]
    avgScore: float


# Define graph

graph = StateGraph(recruitState)

# Define Functions

def tech_feedback(state: recruitState) -> recruitState:

    ans1, ans2, ans3 = state['ans1'], state['ans2'], state['ans3']
    prompt = f"""
                    You are a senior technical recruiter.

                    Evaluate the candidate ONLY on technical skills based on their answers.

                    Scoring Guidelines:
                    - 0-3: Very weak technical understanding
                    - 4-6: Basic knowledge but lacks depth
                    - 7-8: Good understanding with practical exposure
                    - 9-10: Strong depth and real-world experience

                    IMPORTANT:
                    - Focus only on technical skills, tools, and depth
                    - Ignore communication and storytelling
                    - Do NOT give generic feedback

                    Return STRICT JSON only:
                    {{
                    "eval": "<detailed technical feedback in 4-5 sentences>",
                    "score": <integer 0-10>
                    }}

                    Candidate Answers:
                    Q1: {ans1}
                    Q2: {ans2}
                    Q3: {ans3}
                                """

    resp = llmstruct.invoke(prompt)

    return {'techEval': resp.eval, 'individualScores': [resp.score]}

def comm_feedback(state: recruitState) -> recruitState:

    ans1, ans2, ans3 = state['ans1'], state['ans2'], state['ans3']
    prompt = f"""
                    You are a senior recruiter evaluating communication skills.

                    Evaluate the candidate ONLY on communication.

                    Scoring Guidelines:
                    - 0-3: Very unclear, confusing
                    - 4-6: Understandable but lacks clarity/structure
                    - 7-8: Clear and structured
                    - 9-10: Excellent clarity, concise, well-articulated

                    IMPORTANT:
                    - Focus on clarity, structure, and explanation style
                    - Ignore technical correctness
                    - Check if ideas are easy to follow

                    Return STRICT JSON only:
                    {{
                    "eval": "<detailed communication feedback in 4-5 sentences>",
                    "score": <integer 0-10>
                    }}

                    Candidate Answers:
                    Q1: {ans1}
                    Q2: {ans2}
                    Q3: {ans3}
                               """

    resp = llmstruct.invoke(prompt)  

    return {'commEval': resp.eval, 'individualScores': [resp.score]}

def prob_feedback(state: recruitState) -> recruitState:

    ans1, ans2, ans3 = state['ans1'], state['ans2'], state['ans3']
    prompt = f"""
                    You are evaluating problem-solving ability.

                    Focus on:
                    - Logical thinking
                    - Step-by-step approach
                    - Handling unknown situations
                    - Debugging mindset

                    Scoring Guidelines:
                    - 0-3: No clear approach
                    - 4-6: Basic thinking but unstructured
                    - 7-8: Good structured approach
                    - 9-10: Excellent logical and analytical thinking

                    IMPORTANT:
                    - Focus on thinking process, not just result
                    - Evaluate how candidate approaches problems

                    Return STRICT JSON only:
                    {{
                    "eval": "<detailed problem-solving feedback in 4-5 sentences>",
                    "score": <integer 0-10>
                    }}

                    Candidate Answers:
                    Q1: {ans1}
                    Q2: {ans2}
                    Q3: {ans3}
                                """
    
    resp = llmstruct.invoke(prompt)

    return {'probSolvingEval': resp.eval, 'individualScores': [resp.score]}

def redflag_feedback(state: recruitState) -> recruitState:

    ans1, ans2, ans3 = state['ans1'], state['ans2'], state['ans3']
    prompt = f"""
                    You are a hiring manager detecting red flags in a candidate.

                    Check for:
                    - Overconfidence without proof
                    - Vague or fake answers
                    - Blaming others
                    - Lack of ownership
                    - Inconsistencies

                    Scoring Guidelines:
                    - 0-3: Major red flags (reject)
                    - 4-6: Some concerns
                    - 7-8: Minor/no issues
                    - 9-10: Very trustworthy candidate

                    IMPORTANT:
                    - HIGH score = GOOD candidate (NO red flags)
                    - LOW score = BAD candidate (HAS red flags)
                    - Be strict and realistic

                    Return STRICT JSON only:
                    {{
                    "eval": "<detailed red flag analysis>",
                    "score": <integer 0-10>
                    }}

                    Candidate Answers:
                    Q1: {ans1}
                    Q2: {ans2}
                    Q3: {ans3}
                                """

    resp = llmstruct.invoke(prompt)

    return {'redFlagEval': resp.eval, 'individualScores': [resp.score]}

def avg_score(state: recruitState) -> recruitState:

    avg = sum(state['individualScores'])/len(state['individualScores'])
    return {'avgScore': avg}

def advance(state: recruitState) -> recruitState:

    techFeedback, commFeedback = state['techEval'], state['commEval']
    probFeedback, redFlagFeedback = state['probSolvingEval'], state['redFlagEval']
    prompt = f""" The candidate is selected, create a detailed feedback and congratulations message

        technical feedback: {techFeedback}
        communication feedback: {commFeedback}
        problem solving feedback: {probFeedback}
        red flag feedback: {redFlagFeedback}
    
        """
    
    resp = llm.invoke(prompt)

    return {'summary': resp.content}

def reject(state: recruitState) -> recruitState:

    techFeedback, commFeedback = state['techEval'], state['commEval']
    probFeedback, redFlagFeedback = state['probSolvingEval'], state['redFlagEval']
    prompt = f""" The candidate is rejected, create a detailed feedback and rejection message

        technical feedback: {techFeedback}
        communication feedback: {commFeedback}
        problem solving feedback: {probFeedback}
        red flag feedback: {redFlagFeedback}
    
        """
    
    resp = llm.invoke(prompt)

    return {'summary': resp.content}    

def router(state: recruitState) -> Literal['advance','reject']:

    if state['avgScore'] > 7:
        return 'advance'
    else:
        return 'reject'

# Define Nodes

graph.add_node('tech_feedback', tech_feedback)
graph.add_node('comm_feedback', comm_feedback)
graph.add_node('prob_feedback', prob_feedback)
graph.add_node('redflag_feedback', redflag_feedback)
graph.add_node('avg_score', avg_score)
graph.add_node('advance', advance)
graph.add_node('reject', reject)

# Define Edges

graph.add_edge(START, 'tech_feedback')
graph.add_edge(START, 'comm_feedback')
graph.add_edge(START, 'prob_feedback')
graph.add_edge(START, 'redflag_feedback')
graph.add_edge('tech_feedback', 'avg_score')
graph.add_edge('comm_feedback', 'avg_score')
graph.add_edge('prob_feedback', 'avg_score')
graph.add_edge('redflag_feedback', 'avg_score')
graph.add_conditional_edges('avg_score', router)
graph.add_edge('advance', END)
graph.add_edge('reject', END)

# Compile

workflow = graph.compile()

# Invoke

ans1 = """

I have primarily worked with Java and Python. In Java, I have experience building backend logic and solving data structure problems. 
I have also used Python for scripting and building small projects.For frameworks, I have used Flask to build a simple web application 
where users could upload images and get predictions from a machine learning model. I handled routing, API integration, and basic UI connection.
I have also worked with tools like Git and GitHub for version control, and I am familiar with REST APIs and how to integrate them into applications.
In terms of projects, one of my main projects involved building an AI-based system where users upload an image and receive processed output along 
with metadata. This helped me understand backend workflows, API handling, and integrating ML models into applications.

"""

ans2 = """

When I see a problem for the first time, I first try to understand it clearly by breaking it down into smaller parts. I make sure I know the input, 
output, and any constraints given. Then I think about similar problems I have solved before and try to identify patterns or approaches 
that might work. After that, I come up with a basic solution, even if it is not optimal, just to get started.
Once I have a working approach, I try to optimize it by considering time and space complexity. I also test my solution with edge cases to make sure it 
works correctly. If I get stuck, I try to revisit the problem, simplify it further, or look at examples to gain better clarity.

"""

ans3 = """

One time while working on a project, I was integrating a feature where users could upload files and get processed results, 
but the system was not returning the expected output. Initially, I thought the issue was with the frontend, but after checking, I realized the 
problem was in the backend API where the data was not being processed correctly. To handle this, I started debugging step by step, checking logs 
and verifying each part of the workflow. I also broke the problem into smaller parts to identify exactly where it was failing.
After some time, I found that the issue was due to incorrect handling of file data in the API. I fixed it and tested the system again.
This experience taught me the importance of systematic debugging and not making assumptions too quickly.

"""

initial_state = {'ans1': ans1, 'ans2': ans2, 'ans3': ans3}
final_state = workflow.invoke(initial_state)

print('Technical Eval: ' + final_state['techEval'] + '\n')
print('Communication Eval: ' + final_state['commEval'] + '\n')
print('Problem Solving Eval: ' + final_state['probSolvingEval'] + '\n')
print('Red Flag Eval: ' + final_state['redFlagEval'] + '\n')
print('Summary' + final_state['summary'] + '\n')
print(f'Individual Scores: {final_state['individualScores']} \n')
print(f'Avg Score: {final_state['avgScore']}')


# Technical Eval: The candidate demonstrates a solid grasp of programming languages like Java and Python with practical applications such as 
# building web apps using Flask, working on backend logic for data structures in Java, integrating machine learning models into APIs. Familiarity 
# with version control systems (Git/GitHub) indicates good workflow practices; however, the experience described lacks depth concerning advanced 
# topics or cutting-edge frameworks/tools which may limit scoring at a higher level. Overall technical skills are sound but indicate room to expand 
# knowledge beyond intermediate use cases.

# Communication Eval: The candidate communicates their experiences clearly but lacks a structured approach which might make some parts harder for 
# others to follow.

# Problem Solving Eval: The responses display good logical thinking by breaking down problems into smaller parts (Q2), showing an ability to 
# recognize patterns, think analytically about optimization after a basic solution is found. The candidate demonstrates structured approach in Q3 
# with step-by-step troubleshooting which includes reviewing logs and verifying individual components of the workflow – indicative of excellent debugging 
# mindset.

# Red Flag Eval: The candidate's answers show a good balance between confidence and humility without any major red flags detected (score 7-8). 
# They provide detailed explanations for their experiences, indicating both practical knowledge in Java/Python development as well as problem-solving 
# skills. There's no overconfidence; rather they explain the debugging process methodically which shows thoughtful analysis.

# SummarySubject: Congratulations on Your Selection and Feedback Summary!
# Dear [Candidate's Name],
# I hope this message finds you exceptionally well! We are thrilled to have selected you for our team, following a rigorous evaluation of your skills. 
# I would like take some time now just as an opportunity not only to congratulate but also offer feedback that we believe will be beneficial in helping 
# us continue working towards excellence together.
# **Technical Feedback:**
# Firstly and foremost – congratulations on showcasing solid programming proficiency! Your practical experience with Java and Python, particularly 
# building web apps using Flask for the backend logic of data structures is commendable. Integrating machine learning models into APIs has also been a
# significant part of your skill set which indeed reflects excellent technical prowess.

# It was noted that you have demonstrated good familiarity with version control systems like Git/GitHub indicating sound workflow practices – 
# this aspect will be crucial as we work collaboratively on complex projects in the future.
# However, there appears to lack an exposure towards more advanced topics and cutting-edge frameworks/tools. 
# While your skill set currently lies at a commendable intermediate level of technical proficiency; I believe you would benefit from expanding knowledge beyond basic use cases into higher-level applications.

# **Communication Feedback:**
# Your ability for clarity is undeniable – however we observed that the structure in delivering certain parts could be improved upon to ensure 
# seamless comprehension by everyone involved. Striving towards this will undoubtedly prove an asset as our team collaborates on intricate projects 
# involving diverse skill sets of varying levels across a timeline with deadlines and deliverables.

# **Problem Solving Feedback:**
# Your responses have showcased exceptional logical thinking; breaking down problems into smaller manageable parts is indeed commendable (Q2). 
# Your ability to recognize patterns, think analytically about optimization after finding the basic solution was also evident. Notably your structured 
# approach during Q3 troubleshooting displayed an excellent debugging mindset – reviewing logs and verifying individual components of a workflow were 
# insightful.

# **Red Flag Feedback:**
# A balanced blend between confidence in abilities while maintaining humility (score 7-8) is certainly admirable; there are no major red flags 
# detected at this stage. Your detailed explanations for experiences indicate both practical knowledge as well technical problem-solving skills – 
# something that will indeed be beneficial on our team.
# Furthermore, demonstrating thoughtful analysis and a methodical approach to the debugging process was particularly impressive.

# **Closing Thoughts:**
# Your journey into software development seems excitingly promising! As you embark upon this new career path with us I trust your passion for learning as 
# well as adapting would make up any perceived gaps in knowledge. This will also be an opportunity not only on personal growth but our collective success 
# too!
# As we move forward, remember that continuous self-improvement is key; don't hesitate to seek opportunities from colleagues or online platforms like 
# Coursera and Udemy which offer courses for advanced learning.
# Once again – Congratulations! We are excited about joining forces with you. Looking eagerly towards what lies ahead in this exciting new chapter of 
# our careers!

# Wishing many more successes,

# [Your Name]
# [Your Position]

# P.S: Feel free to share any queries or thoughts you'd like us to address as we move forward together on the next stage!

# Individual Scores: [6, 9, 9, 7]

# Avg Score: 7.75