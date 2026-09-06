from chains.query_analyzer_chain import query_analyzer_chain
from chains.query_expansion_chain import query_expansion_chain
from chains.query_decomposition_chain import query_decomposition_chain

from graph.state import RAGState



def analyze_query(state: RAGState) -> dict:
    """Analyze the user's query and update the state."""

    query = state["original_query"]

    analysis = query_analyzer_chain.invoke({
        "query": query
    })

    # Make entity extraction more reliable for known technical terms.
    known_entities = [
        "RAG",
        "retrieval-augmented generation",
        "LLM",
        "LLMs",
        "RLHF",
        "DPO",
        "BM25",
        "vector",
        "graph",
        "knowledge grounding",
    ]

    query_lower = query.lower()

    detected_entities = [
        entity
        for entity in known_entities
        if entity.lower() in query_lower
    ]

    # Use deterministic entities when the LLM misses them.
    if detected_entities:
        analysis.entities = detected_entities

    return {
        "analysis": analysis
    }




def expand_query(state: RAGState) -> dict:
    """Expand the user's query and update the state."""

    expansion = query_expansion_chain.invoke({
        "query": state["original_query"]
    })

    return {
        "expansion": expansion
    }

def decompose_query(state: RAGState) -> dict:
    """Decompose the user's query and update the state."""

    decomposition = query_decomposition_chain.invoke({
        "query": state["original_query"]
    })

    return {
        "decomposition": decomposition
    }