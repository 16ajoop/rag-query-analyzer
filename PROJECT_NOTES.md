# RAG Query Analyzer

## 1. Project Overview

This project is building a **Retrieval-Augmented Generation (RAG) system** that intelligently analyzes a user's query before retrieving information and generating an answer.

The goal is to create a retrieval pipeline that can choose appropriate strategies depending on the query.

The overall architecture is:

```text
                    DOCUMENTS
                       │
                       ▼
                  Ingestion
                       │
                       ▼
                    Chunking
                       │
                       ▼
                   Embeddings
                       │
                       ▼
                   Vector DB
                       │
                       │
                       │
USER QUERY ────────────┘
     │
     ▼
Query Analyzer
     │
     ├───────────────┐
     ▼               ▼
Query Expansion   Query Decomposition
     │               │
     └───────┬───────┘
             ▼
         Retrieval
       ┌─────┼─────┐
       ▼     ▼     ▼
     BM25  Vector  Graph
       └─────┼─────┘
             ▼
        Fusion / RRF
             │
             ▼
         Reranking
             │
             ▼
       Context Builder
             │
             ▼
        LLM Generation
```

---

# 2. Main Components

The system can be divided into two major sides.

### Document Side

This prepares documents so that they can later be searched.

```text
Documents
    ↓
Ingestion
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
```

### Query Side

This processes the user's question and retrieves the most relevant information.

```text
User Query
    ↓
Query Analyzer
    ↓
Query Expansion
    ↓
Query Decomposition
    ↓
Retrieval
    ↓
Fusion / RRF
    ↓
Reranking
    ↓
Context Builder
    ↓
LLM Generation
```

---

# 3. Technologies and Dependencies

The main packages used in this project are:

| Package            | Remember it as            | Purpose in this project               |
| ------------------ | ------------------------- | ------------------------------------- |
| `langchain`        | 🧰 LLM Toolkit            | Building LLM-based components         |
| `langchain-core`   | 🧱 Foundation             | Prompts, chains, interfaces, LCEL     |
| `langchain-ollama` | 🌉 Bridge                 | Connects LangChain with Ollama        |
| `langgraph`        | 🗺️ Workflow              | Orchestrates the RAG workflow         |
| `pydantic`         | 📋 Structure & Validation | Defines and validates data structures |
| `python-dotenv`    | 🔐 Configuration          | Loads settings from `.env`            |

---

# 4. Understanding the Dependencies

## 4.1 LangChain

`langchain` is a framework for building applications around Large Language Models.

It provides building blocks for things such as:

* LLMs
* Prompts
* Chains
* Agents
* Structured outputs
* Retrieval
* Tools

Think of LangChain as a **toolkit for building LLM applications**.

---

## 4.2 LangChain Core

`langchain-core` contains the fundamental abstractions used by LangChain.

For example:

* `ChatPromptTemplate`
* Messages
* Runnable interfaces
* LCEL

### LCEL

LCEL stands for **LangChain Expression Language**.

It provides a declarative way to connect components using the pipe operator `|`.

For example:

```python
chain = prompt | model | output_parser
```

The output of one component automatically becomes the input of the next component.

Conceptually:

```text
Prompt
  │
  ▼
LLM
  │
  ▼
Output Parser
```

The `|` operator is similar to the idea of Unix command-line pipelines, where the output of one command is passed to another.

---

## 4.3 LangChain Ollama

`langchain-ollama` provides the connection between LangChain and Ollama.

In this project:

```text
LangChain
    │
    ▼
langchain-ollama
    │
    ▼
Ollama
    │
    ▼
Local LLM
```

This allows the project to use an Ollama-hosted model inside LangChain chains.

---

## 4.4 LangGraph

LangGraph is used to build and orchestrate the workflow.

While LangChain provides many of the **building blocks**, LangGraph controls **how those components execute and interact**.

For example:

```text
START
  ↓
Query Analyzer
  ↓
Query Router
  ↓
 ┌───────────────┐
 │               │
 ▼               ▼
Expansion    Decomposition
 │               │
 └───────┬───────┘
         ▼
     Retrieval
         ↓
        RRF
         ↓
      Reranker
         ↓
      Generation
         ↓
        END
```

A useful way to remember this is:

> **LangChain = tools/components**
> **LangGraph = workflow/orchestration**

---

# 5. Pydantic

Pydantic is used to define structured data and validate it.

For example:

```python
age: int
```

means the `age` field should contain an integer.

We can also restrict a field to specific values using `Literal`.

For example:

```python
intent: Literal[
    "factual",
    "explanation",
    "comparison"
]
```

This means `intent` must be one of the allowed values.

---

# 6. BaseModel

In this project, I created my own Pydantic model called:

```python
QueryAnalysis
```

It inherits from:

```python
BaseModel
```

For example:

```python
from pydantic import BaseModel

class QueryAnalysis(BaseModel):
    ...
```

### What is BaseModel?

`BaseModel` is the foundation provided by Pydantic for creating structured, validated models.

A useful mental model is:

```text
BaseModel
    ↓
provides the Pydantic model behavior
    ↓
My custom model
    ↓
QueryAnalysis
```

Another way to think about it:

> **BaseModel is the foundation/rule system on which I build my own structured model.**

Pydantic then uses the rules defined in my model to validate the data.

---

# 7. Python-dotenv

`python-dotenv` is used to load environment variables from a `.env` file.

For example:

```text
.env
 │
 ▼
python-dotenv
 │
 ▼
Application configuration
```

The `.env` file can contain configuration such as:

* API keys
* Model names
* Model configuration
* Other environment-specific settings

This allows configuration to remain separate from the Python source code.

---

# 8. Query Analysis

Before retrieval happens, the user's query is analyzed.

The purpose of the Query Analyzer is to understand the characteristics of the query and determine how it should be processed.

For example, the analyzer can identify things such as:

* Intent
* Complexity
* Entities
* Whether query expansion is needed
* Whether decomposition is needed

The analyzer produces a structured result using the `QueryAnalysis` Pydantic model.

Conceptually:

```text
User Query
    ↓
Query Analyzer
    ↓
QueryAnalysis
```

The Pydantic model ensures that the analyzer's output follows the expected structure.

---

# 9. Prompt + LangChain + Ollama

The Query Analyzer works through several layers.

```text
Pydantic Model
      ↑
      │
Structured Output
      ↑
      │
     LLM
      ↑
      │
    Prompt
```

The LangChain chain connects these components.

Conceptually:

```text
Prompt
  ↓
Ollama LLM
  ↓
Structured Output
  ↓
QueryAnalysis
```

Therefore:

> **Pydantic → defines the structure**
> **Prompt → tells the LLM what to analyze**
> **LangChain → connects prompt + LLM + structured output**

---

# 10. LangGraph State

The workflow contains multiple components:

```text
User Query
    ↓
Analyzer
    ↓
Expansion
    ↓
Decomposition
    ↓
Retrieval
```

Each component needs information from previous components.

For example:

* The Analyzer needs the original query.
* Expansion needs the query and/or analysis.
* Decomposition needs the query and/or analysis.
* Retrieval needs the processed query information.

Therefore, the workflow needs a place to store this information.

That is the purpose of **State**.

---

# 11. What is State?

State is the shared information that travels through the LangGraph workflow.

Each node can:

1. Read information from the state.
2. Perform its task.
3. Add or update information in the state.

Conceptually:

```text
              RAGState
        ┌──────────────────┐
        │ original_query   │
        │ analysis         │
        │ expansion        │
        │ decomposition    │
        └──────────────────┘
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   Analyzer  Expansion  Decomposition
       │         │         │
       └─────────┴─────────┘
                 │
                 ▼
           Updated State
```

So, State acts like the **shared memory of the workflow**.

---

# 12. LangGraph Nodes

A node represents a specific task in the workflow.

Examples:

* Analyzer node
* Expansion node
* Decomposition node
* Retrieval node
* Reranking node
* Generation node

A node generally follows this pattern:

```text
Read State
    ↓
Perform Task
    ↓
Return Updated State
```

For example:

```text
State
  ↓
Analyzer Node
  ↓
Analyze Query
  ↓
Add Analysis to State
  ↓
Updated State
```

---

# 13. Conditional Routing

Not every query needs the same processing.

For example:

```text
                    Query
                      ↓
                  Analyzer
                      ↓
                Query Router
                 /         \
                /           \
               ▼             ▼
          Expansion      Decomposition
                \           /
                 \         /
                  ▼       ▼
                   Retrieval
```

The analyzer determines what should happen next.

This is implemented using **conditional edges** in LangGraph.

Therefore:

> **Nodes perform tasks.**
> **State carries information.**
> **Conditional edges decide where the workflow goes next.**
> **LangGraph orchestrates everything.**

---

# 14. Current Project Status

The following components have been completed:

* ✅ Pydantic models
* ✅ Query Analyzer chain
* ✅ Query Expansion chain
* ✅ Query Decomposition chain
* ✅ LangGraph State
* ✅ LangGraph nodes
* ✅ Conditional routing
* ✅ Tested simple query
* ✅ Tested decomposition path

The query-processing portion of the project is therefore working up to the point where it can determine how a query should be processed.

---

# 15. Current Architecture

The part implemented so far can be summarized as:

```text
User Query
    ↓
Query Analyzer
    ↓
Query Expansion
    ↓
Query Decomposition
    ↓
Conditional Routing
    ↓
Retrieval
```

The retrieval layer is the next major stage.

---

# 16. Next Stage: Retrieval

After query analysis, expansion, and decomposition, the system needs to actually **retrieve relevant information**.

The planned retrieval architecture is:

```text
                 Retrieval
              ┌─────┼─────┐
              ▼     ▼     ▼
            BM25  Vector  Graph
              └─────┼─────┘
                    ▼
                Fusion
                  / RRF
                    ↓
                 Reranker
                    ↓
              Context Builder
                    ↓
               LLM Generation
```

The three retrieval methods are:

### BM25

A keyword-based retrieval method.

It is useful when exact words, terms, or phrases are important.

### Vector Search

A semantic retrieval method based on embeddings.

It is useful when the meaning of the query is more important than exact keyword matching.

### Graph Search

A retrieval method that uses relationships between entities and information represented in a graph.

---

# 17. Why Multiple Retrieval Methods?

Different retrieval methods have different strengths.

For example:

```text
                 User Query
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        BM25       Vector      Graph
          │          │          │
     Keywords     Meaning    Relationships
          │          │          │
          └──────────┼──────────┘
                     ▼
                   Fusion
```

Instead of relying on only one retrieval strategy, the system can combine the results from multiple retrievers.

This should improve the chances of finding useful context.

---

# 18. Fusion / RRF

The results from BM25, vector search, and graph search need to be combined.

The planned approach is:

**RRF — Reciprocal Rank Fusion**

Conceptually:

```text
BM25 Results
     │
     ├────────┐
Vector Results│
     │        │
     ├────────┤
Graph Results│
     │        │
     └────┬───┘
          ▼
         RRF
          │
          ▼
 Combined Ranked Results
```

The purpose of RRF is to combine rankings from different retrieval systems into one ranking.

---

# 19. Reranking

After fusion, the retrieved documents are not necessarily in their final order.

A **reranker** can examine the query and retrieved documents more carefully and reorder them according to relevance.

```text
Retrieved Results
       ↓
      RRF
       ↓
   Reranking
       ↓
Most Relevant Results
```

---

# 20. Context Builder

The reranked documents are then converted into the context that will be given to the LLM.

```text
Reranked Documents
        ↓
   Context Builder
        ↓
Relevant Context
        ↓
       LLM
```

The Context Builder is responsible for creating a clean, useful context from the retrieved information.

---

# 21. Final Generation Pipeline

The complete planned RAG pipeline is:

```text
                         DOCUMENTS
                            │
                            ▼
                       Ingestion
                            │
                            ▼
                        Chunking
                            │
                            ▼
                       Embeddings
                            │
                            ▼
                        Vector DB
                            │
                            │
                            │
USER QUERY ────────────────┘
     │
     ▼
Query Analyzer
     │
     ▼
Query Expansion
     │
     ▼
Query Decomposition
     │
     ▼
   Retrieval
  ┌──┼──────┐
  ▼  ▼      ▼
BM25 Vector Graph
  └──┼──────┘
     ▼
   RRF/Fusion
     │
     ▼
  Reranking
     │
     ▼
Context Builder
     │
     ▼
LLM Generation
     │
     ▼
   Answer
```

---

# 22. Important Mental Model

The entire project can be remembered using these roles:

```text
Pydantic
    ↓
Defines the structure

Prompt
    ↓
Defines what the LLM should do

LangChain
    ↓
Connects the LLM components

Nodes
    ↓
Perform individual workflow tasks

State
    ↓
Carries information between nodes

Conditional Edges
    ↓
Decide which node runs next

LangGraph
    ↓
Orchestrates the complete workflow

Retrieval
    ↓
Finds relevant information

RRF / Fusion
    ↓
Combines retrieval results

Reranker
    ↓
Orders results by relevance

Context Builder
    ↓
Prepares information for the LLM

LLM
    ↓
Generates the final answer
```

---

# 23. Current Position in the Project

The project has completed the **query-processing and workflow foundation**.

```text
                 PROJECT PROGRESS

Document Processing
        │
        ├── Ingestion          ⏳
        ├── Chunking           ⏳
        ├── Embeddings         ⏳
        └── Vector DB          ⏳
        
Query Processing
        │
        ├── Query Analyzer     ✅
        ├── Query Expansion    ✅
        ├── Decomposition      ✅
        ├── State              ✅
        ├── Nodes              ✅
        └── Routing            ✅

Retrieval
        │
        ├── BM25               ⏳
        ├── Vector Search      ⏳
        ├── Graph Search       ⏳
        ├── RRF / Fusion       ⏳
        └── Reranking          ⏳

Generation
        │
        ├── Context Builder    ⏳
        └── LLM Generation     ⏳
```

## Next Goal

The next stage is to build the **retrieval layer**, beginning with the document-processing pipeline and then implementing:

```text
Documents
   ↓
Ingestion
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector DB
   ↓
BM25 + Vector + Graph Retrieval
   ↓
RRF
   ↓
Reranking
   ↓
Context Builder
   ↓
LLM
```
