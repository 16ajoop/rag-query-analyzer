from langgraph.graph import StateGraph, START, END

from graph.state import RAGState
from graph.nodes import (
    analyze_query,
    expand_query,
    decompose_query,
)


# 1. Create the graph
builder = StateGraph(RAGState)



# 2. Add  nodes
builder.add_node("analyze", analyze_query)
builder.add_node("expand", expand_query)
builder.add_node("decompose", decompose_query)



# 3. Connect START to analyzer
builder.add_edge(START, "analyze")



# 4. Decide what to do after analysis
def route_after_analysis(state: RAGState) -> str:

    analysis = state["analysis"]

    if analysis is None:
        return "end"
    if analysis.needs_expansion:
        return "expand"
    if analysis.needs_decomposition:
        return "decompose"
    
    return "end"



# 5. Conditional routing after analyzer
builder.add_conditional_edges(
    "analyze",
    route_after_analysis,
    {
        "expand": "expand",
        "decompose": "decompose",
        "end": END,
    },
)



# 6. Decide what to do after expansion
def route_after_expansion(state: RAGState) -> str:

    analysis = state["analysis"]

    if analysis is not None and analysis.needs_decomposition:
        return "decompose"
    
    return "end"



# 7. Conditional routing after expansion
builder.add_conditional_edges(
    "expand",
    route_after_expansion,
    {
        "decompose": "decompose",
        "end": END,
    },
)



# 8. Decomposition finishes this stage
builder.add_edge("decompose", END)


# 9. Compile the graph
workflow = builder.compile()



