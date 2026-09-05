from chains.query_analyzer_chain import query_analyzer_chain
from chains.query_expansion_chain import query_expansion_chain
from chains.query_decomposition_chain import query_decomposition_chain

from graph.state import RAGState



def analyze_query(state: RAGState) -> dict:
    """Analyze the user's query and update the state."""

    analysis = query_analyzer_chain.invoke({
        "query": state["original_query"]
    })

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