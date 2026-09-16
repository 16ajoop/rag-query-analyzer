# RAG Query Analyzer

A Retrieval-Augmented Generation (RAG) system that analyzes user queries and uses multiple retrieval strategies to find relevant information before generating an answer.

The project explores how query analysis, hybrid retrieval, ranking, and LLM generation can be combined to build a more effective RAG pipeline.


## Architecture

## Key Features 

The system follows these steps to process a user query and generate a relevant, grounded answer:

### 1. Query Analysis

Analyzes the user's query using structured LLM output to identify intent, complexity, entities, and retrieval requirements.

### 2. Query Expansion

Generates additional relevant terms or variations to improve retrieval coverage.

### 3. Query Decomposition

Breaks complex questions into smaller sub-queries when necessary.

### 4. Intelligent Routing

Uses **LangGraph conditional routing** to determine the appropriate processing path for the query.

### 5. Document Processing

Loads documents, splits them into meaningful chunks, and prepares them for retrieval.

### 6. Embedding Generation

Converts document chunks into semantic vector representations using **Ollama embeddings**.

### 7. Vector Retrieval

Stores embeddings in **ChromaDB** and retrieves documents based on semantic similarity.

### 8. BM25 Retrieval

Performs keyword-based retrieval to capture exact terms and phrases that semantic search may miss.

### 9. Hybrid Retrieval & RRF

Combines vector and BM25 results using **Reciprocal Rank Fusion (RRF)** to produce a unified ranking.

### 10. Reranking

Reranks the retrieved candidates based on their relevance to the original query.

### 11. Context Building

Selects and organizes the most relevant retrieved information into a clean context for the LLM.

### 12. LLM Generation

Provides the user query and retrieved context to the LLM to generate a **grounded final answer**.

### 13. Workflow Orchestration

Uses **LangGraph** to manage state, nodes, and the complete end-to-end RAG workflow.


## Tech Stack
- Python
- LangChain
- LangGraph
- Ollama
- Llama 3.2
- nomic-embed-text
- ChromaDB
- BM25
- Pydantic


## Tech Stack
        Technology	                                       Purpose
        
        Python	                                           Core development
        LangChain	                                         LLM and RAG components
        LangGraph	                                         Workflow orchestration
        Ollama	                                           Local LLM and embedding models
        Llama 3.2	                                         Local LLM
        nomic-embed-text	                                 Text embeddings
        ChromaDB	                                         Vector database
        BM25	                                             Keyword-based retrieval
        Pydantic	                                         Data validation and structured output
## How It Works

### 1. Document Processing
Documents are loaded, split into smaller chunks, converted into embeddings, and stored in Chroma.

    Documents
       ↓
    Loading
       ↓
    Chunking
       ↓
    Embeddings
       ↓
    Chroma Vector DB

### 2. Query Processing
The user's query is analyzed before retrieval.

          User Query 
              ↓ 
          Query Analyzer 
              ↓ 
    Expansion / Decomposition 
              ↓ 
          Conditional Routing

### 3. Hybrid Retrieval
The system combines semantic and keyword-based retrieval.

              User Query
                   │
          ┌────────┴────────┐
          ▼                 ▼
     Vector Search        BM25
          │                 │
          └────────┬────────┘
                   ▼
                  RRF
                   │
                   ▼
              Reranking
              
### 4. Reciprocal Rank Fusion
RRF combines the rankings produced by different retrieval methods.

    Vector Results ──┐
                     ├──→ RRF → Combined Ranking
    BM25 Results ────┘

This allows results from multiple retrieval approaches to be combined into a single ranked list.

### 5. Reranking
The fused results are passed through a reranking stage to identify the most relevant chunks for the query.

    RRF Results
         ↓
    Reranker
         ↓
    Ranked Relevant Chunks
    
### 6. Context Building and Generation
The highest-ranked chunks are combined into the final context and provided to the LLM.

            Reranked Results
                   ↓
            Context Builder
                   ↓
            Final Context
                   ↓
              Llama 3.2
                   ↓
              Final Answer

## Project Structure

        rag-query-analyzer/
        |
        |── agent/
        |   ├── graph.py
        │   ├── states.py
        │   ├── prompts.py
        │   └── tools.py
        │
        ├── data/
        │   └── documents/
        │
        ├── generated_project/
        │
        ├── main.py
        ├── requirements.txt
        ├── .env
        ├── .gitignore
        └── README.md

## Project Outcome

The completed project demonstrates a full RAG workflow that goes beyond basic vector search by combining query understanding, hybrid retrieval, ranking, and LLM-based generation into a single workflow.

Built as a hands-on project to understand and implement an end-to-end RAG architecture using local LLMs and retrieval components.
