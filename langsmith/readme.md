# 📊 LangSmith Tracking Examples

This folder contains practical examples of integrating **LangSmith** with LangChain-based workflows to enable **tracing, debugging, and observability** in LLM applications.

While the main repository focuses on **LangGraph and agentic AI workflows**, this folder demonstrates how to monitor and analyze simpler pipelines using LangSmith.

---

## 🚀 What’s Inside

This folder includes implementations of:

- 🔗 Simple LLM Chains  
- 🧠 Sequential Chains  
- 📚 Basic RAG (Retrieval-Augmented Generation) Pipelines  
- 🧪 Experiments for tracing and debugging  

Each example is instrumented with **LangSmith tracing**, allowing you to:

- Visualize execution flows  
- Track inputs and outputs  
- Debug intermediate steps  
- Analyze latency and performance  

---

## 🧠 Why This Matters

As AI systems grow more complex (especially with **agents and LangGraph workflows**), debugging becomes harder.

LangSmith helps you:

- Understand how your chains and agents behave  
- Identify bottlenecks and hallucinations  
- Improve reliability and production readiness  

This folder builds the **foundation for observability**, which is critical before moving to advanced agent workflows.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yuvraj-kumar-dev/LangGraph-Workflows.git
cd LangGraph-Workflows/langsmith
```

### 2. Configure Environment Variables

#### Create a .env file in this folder and add:

```
GROQ_API_KEY="your-groq-api-key"
LANGCHAIN_API_KEY="your-langsmith-api-key"
LANGCHAIN_TRACING=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_PROJECT="your-project-name"
```

### ▶️ Running Examples

Run any script:
```
python filename.py
```
Once executed, traces will automatically appear in your LangSmith dashboard.


### 📈 Viewing Traces
Go to: https://smith.langchain.com
Open your project (LANGCHAIN_PROJECT)

Explore:
- Execution graphs
- Inputs/outputs
- Latency breakdown
- Debug traces