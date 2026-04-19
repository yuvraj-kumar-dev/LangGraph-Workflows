from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(model='llama-3.1-8b-instant')

prompt = PromptTemplate.from_template("{question}")
parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({"question": "What is the capital of India"})
print(result)