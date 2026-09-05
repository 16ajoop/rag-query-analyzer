from langgraph.graph import StateGraph, START, END

from graph.state import RAGState
from graph.nodes import (
    analyze_query,
    expand_query,
    decompose_query,
)


# 1. Create the graph
builder = StateGraph(RAGState)



# 2. Add our nodes
builder.add_node("analyze", analyze_query)
builder.add_node("expand", expand_query)
builder.add_node("decompose", decompose_query)



#3. Connect the nodes
builder.add_edge(START, "analyze")
builder.add_edge("analyze", "expand")
builder.add_edge("expand", "decompose")
builder.add_edge("decompose", END)



# 4. Compile the graph
workflow = builder.compile()




