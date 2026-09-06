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
        ├── Ingestion          ✅
        ├── Chunking           ✅
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


## Documents side:

Documents
   ↓
Ingestion
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector DB

# What is chunking?

Suppose we have a large document:

Document
│
├── Introduction
├── RAG architecture
├── Retrieval
├── Embeddings
├── Hallucinations
├── Evaluation
└── Conclusion

We don't want to put the entire document into the vector database as one huge piece.

Instead:

Document
   ↓
Chunking
   ↓
┌──────────────┐
│   Chunk 1    │
├──────────────┤
│   Chunk 2    │
├──────────────┤
│   Chunk 3    │
├──────────────┤
│   Chunk 4    │
└──────────────┘

Each chunk can then receive its own embedding.

Why not just use the whole document?

Imagine the user asks:

"How does RAG reduce hallucinations?"

If your document is 50 pages long, retrieving the entire 50 pages is inefficient.

Instead, we want something like:

Query
 ↓
"How does RAG reduce hallucinations?"
 ↓
Vector search
 ↓
Chunk 17 ← relevant
Chunk 32 ← relevant
Chunk 41 ← relevant

Then only those relevant pieces are sent further down the pipeline.

The important concept: chunk size

We need to decide how much text goes into each chunk.

For example:

chunk_size = 500

roughly means:

Each chunk can contain around 500 characters/tokens depending on the splitter.

What about overlap?

There's another important concept:

Chunk 1
████████████████████

             ████████████████████
             Chunk 2

A small part of Chunk 1 is repeated in Chunk 2.

This is called chunk overlap.

Why?

Because important information can sit exactly at the boundary:

Chunk 1:
"RAG retrieves external information and provides it..."

Chunk 2:
"...provides it to the language model as context."

Without overlap, the meaning might get separated.

# Embeddings

Think of a chunk like:
"RAG retrieves relevant information from an external knowledge source..."

An embedding model converts that text into a vector such as:
[0.021, -0.184, 0.736, 0.092, ...] The actual vector will have many dimensions.

We can use an Ollama embedding model locally.
A commonly used choice is:
nomic-embed-text

LLM ≠ Embedding model
They perform different jobs.

Next step: Create the embedding model

Our pipeline is currently:

                                        Document
                                        ↓
                                        Load
                                        ↓
                                        Chunking
                                        ↓
                                        Embedding  ← WE ARE HERE
                                        ↓
                                        Vector DB

nomic-embed-text converted the meaning of that text into 768 numbers:

Text
 ↓
nomic-embed-text
 ↓
[768 numbers] Those numbers are not something we interpret individually nstead, we compare vectors.

For example:

"RAG reduces hallucinations"
        ↓
     Vector A

"Retrieval augmented generation helps prevent false answers"
        ↓
     Vector B

Because these sentences have similar meanings, their vectors should be close to each other.

Whereas:

"How to cook biryani"
        ↓
     Vector C

would be much farther away.

That's the fundamental idea behind semantic/vector search.

We need to connect our existing chunks to the embedding model:
                        rag.txt
                        ↓
                        load_documents()
                        ↓
                        chunk_documents()
                        ↓
                        chunks
                        ↓
                        nomic-embed-text
                        ↓
                        vector representations

Then we'll store those vectors in a vector database.


# Vector Database
We'll use Chroma because it's simple, local, and suitable for learning this RAG pipeline

Right now we have:
                                            rag.txt
                                            ↓
                                            Loader
                                            ↓
                                            Chunks
                                            ↓
                                            nomic-embed-text
                                            ↓
                                            768-dimensional vectors


Now Chroma will store: 
┌─────────────────────────────────┐
│         Vector Database         │
│                                 │
│ Chunk 1                         │
│   ├── Text                      │
│   ├── Embedding [768 numbers]   │
│   └── Metadata                  │
│                                 │
│ Chunk 2                         │
│   ├── Text                      │
│   ├── Embedding [768 numbers]   │
│   └── Metadata                  │
└─────────────────────────────────┘

The important idea is:

The vector database stores the chunks together with their embeddings so that we can later search for chunks whose meanings are closest to a user's query.

now have:

Documents
    ↓
Loading              ✅
    ↓
Chunking             ✅
    ↓
Embedding            ✅
    ↓
Chroma Vector DB     ✅

The next important step is to actually search the Vector DB.

What we'll test

Suppose the user asks:

How does RAG reduce hallucinations?

We'll do:

                                    User Query
                                        ↓
                                    nomic-embed-text
                                        ↓
                                    Query Vector
                                        ↓
                                    Chroma
                                        ↓
                                    Find most similar chunks
                                        ↓
                                    Relevant document

This is your first real semantic retrieval step.

We'll create a retrieval function that takes a query and returns the most relevant chunks.

The vector database should be created during the ingestion/indexing stage, not every time a user searches.

Our architecture should be:
                 INDEXING TIME
                     
Documents
   ↓
Load
   ↓
Chunk
   ↓
Embedding
   ↓
Chroma DB
        │
        │
        ▼
   ┌───────────┐
   │ Vector DB │
   └───────────┘
        │
        │
                 QUERY TIME
        │
User Query
   ↓
Embedding
   ↓
Similarity Search
   ↓
Relevant Chunks

🧠 Remember this distinction

This is an important RAG concept:

Indexing

Documents → Chunks → Embeddings → Vector DB

happens when you prepare your knowledge base.

Retrieval

Query → Query Embedding → Vector DB → Similar Chunks

happens whenever a user asks a question.


# retrieval
BM25 retrieval.

                        Documents
                        ↓
                        Load             ✅
                        ↓
                        Chunk            ✅
                        ↓
                        Embedding        ✅
                        ↓
                        Chroma           ✅
                        ↓
                        Vector Retrieval ← DONE


Vector search vs BM25

Suppose your document contains:

"Retrieval-Augmented Generation (RAG) combines information retrieval with language generation."

User asks:

"What is RAG?"

Vector search is good because it understands semantic meaning.

But imagine the user asks:

"Find information specifically about RLHF."

Here, exact terminology matters.

That's where BM25 helps:

                    Retrieval
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        Vector Search          BM25
        semantic meaning       keywords
             │                   │
             └─────────┬─────────┘
                       ↓
                    Fusion

This is why your assignment calls for both semantic + keyword retrieval.

What is happening here?

First, our chunks are converted into words:

"RAG reduces hallucinations"
             ↓
["rag", "reduces", "hallucinations"]

BM25 then builds a keyword-based search index.

When the user asks:

"How does RAG reduce hallucinations?"

we convert that too:

["how", "does", "rag", "reduce", "hallucinations"]

BM25 looks for chunks containing important matching words.

Documents
    ↓
Ingestion              ✅
    ↓
Chunking (500)         ✅
    ↓
Embeddings             ✅
    ↓
Vector DB              ✅
    ↓
Vector Retrieval       ✅
    ↓
BM25 Retrieval         ✅

One important observation

You only have one chunk, so both methods return the same document.

That's expected.

For example, with multiple chunks:

Chunk 1 → RAG introduction
Chunk 2 → RLHF
Chunk 3 → DPO
Chunk 4 → Hallucination evaluation
Chunk 5 → Verification methods

A query like:

"What are methods for reducing hallucinations?"

might produce different rankings:

Vector Search
→ Chunk 4
→ Chunk 5
→ Chunk 1

BM25
→ Chunk 1
→ Chunk 4
→ Chunk 5

That's where combining them becomes useful.

🚀 Next: Hybrid Retrieval

Your assignment specifically calls for hybrid retrieval:

             User Query
                  ↓
          ┌───────┴───────┐
          ↓               ↓
       Vector            BM25
       Search            Search
          ↓               ↓
       Results          Results
          └───────┬───────┘
                  ↓
              Fusion
                  ↓
                 RRF

RRF (Reciprocal Rank Fusion) is the next concept we'll implement.

But before coding RRF, we'll first modify our test data to contain multiple meaningful chunks. Otherwise, we won't be able to see why hybrid retrieval and RRF are useful.

So the next step will be:

Expand rag.txt into a small realistic RAG dataset → recreate the vector DB → test Vector vs BM25.

Vector Search
1. Hallucinations
2. RAG
3. RLHF + DPO

Vector search understood the meaning of:

“methods can reduce hallucinations”

So it found concepts related to hallucinations and methods.

BM25
1. Hallucinations
2. RAG
3. Hybrid Retrieval + Graph Retrieval

BM25 focuses more on matching words such as:

methods
reduce
hallucinations
language
models

So its ranking is different.

Why combine them?

Imagine the user asks:

"Compare RAG, RLHF and DPO for reducing hallucinations."

We want:

semantic understanding → Vector
exact method names → BM25

So instead of choosing one:

Vector OR BM25

we use:

Vector + BM25
       ↓
     RRF
       ↓
Combined ranking

And RRF is the next thing we're going to implement.

🧠 RRF in simple terms

Suppose the two retrievers give:

Vector:

Rank 1 → Hallucinations
Rank 2 → RAG
Rank 3 → RLHF/DPO

and:

BM25:

Rank 1 → Hallucinations
Rank 2 → RAG
Rank 3 → Hybrid Retrieval

RRF asks:

"Which documents consistently appear near the top across different retrieval methods?"

A simplified RRF score is:

## score = 1 / (k + rank)

So:

Rank 1 → higher score
Rank 2 → slightly lower
Rank 3 → lower

If a document appears near the top in both Vector and BM25, its scores are added.

Conceptually:

             Vector       BM25
               ↓           ↓
            Rank list   Rank list
               ↓           ↓
               └─────┬─────┘
                     ↓
                    RRF
                     ↓
              Combined ranking

This is why RRF is useful: we don't need the two retrievers to agree on the exact ranking. We combine their rankings.

pipeline now

You've built a significant portion of the retrieval layer:

                         User Query
                             ↓
                    Query Analyzer ✅
                             ↓
               Expansion / Decomposition
                             ↓
                    ┌────────┴────────┐
                    ↓                 ↓
              Vector Search         BM25
                    ↓                 ↓
                    └────────┬────────┘
                             ↓
                            RRF ✅
                             ↓
                       Reranking ← NEXT
What is reranking?

RRF gives us a candidate list.

For example:

RRF
 ↓
10 candidate chunks

But RRF only knows:

"These chunks ranked highly in the retrievers."

It doesn't deeply judge:

"Which chunk is actually the best answer to this particular query?"

A reranker does that.

Conceptually:

Query
  +
Retrieved Chunk
  ↓
Reranker
  ↓
Relevance Score

For example:

Query:
"What methods reduce hallucinations?"

Candidate A → 0.94
Candidate B → 0.81
Candidate C → 0.63
Candidate D → 0.41

Then we keep the highest-scoring chunks.

So the next pipeline becomes:

Vector ──┐
         ├── RRF ──→ Candidate chunks ──→ Reranker
BM25 ────┘


🧠 What is the reranker doing?

RRF has already given us candidates:

RRF
 ↓
Candidate 1
Candidate 2
Candidate 3
Candidate 4
Candidate 5

Now we send each candidate + the original query to the LLM:

Query + Document 1
       ↓
    llama3.2
       ↓
      9/10

Query + Document 2
       ↓
    llama3.2
       ↓
      6/10

Query + Document 3
       ↓
    llama3.2
       ↓
      8/10

Then:

9/10 → Document 1
8/10 → Document 3
6/10 → Document 2

We return the highest-scoring documents.

Now your retrieval pipeline is complete
User Query
    ↓
Query Analyzer
    ↓
Expansion / Decomposition
    ↓
┌───────────────┬───────────────┐
│               │
Vector          BM25
Search          Search
│               │
└───────┬───────┘
        ↓
       RRF
        ↓
    Reranker
        ↓
  Context Builder
        ↓
    Final Context
        ↓
   LLM Generation  ← next

The next step is the final LLM Generation, where we'll take:

User Query + Final Context
          ↓
       llama3.2
          ↓
      Final Answer

      🚀 Next: LLM Generation

Now we're at the final major stage:

User Query
    ↓
Query Analyzer
    ↓
Expansion / Decomposition
    ↓
Vector + BM25
    ↓
RRF
    ↓
Reranker
    ↓
Context Builder
    ↓
⭐ LLM Generation
    ↓
Final Answer


Retrieve relevant information → give it to the LLM → generate a grounded answer.

You've already tested:

✅ Query Analyzer
✅ Query Expansion
✅ Query Decomposition
✅ Document Ingestion
✅ Chunking
✅ Embeddings
✅ Vector Retrieval
✅ BM25
✅ RRF
✅ Reranking
✅ Context Builder