from graph.workflow import workflow


user_query = """
What is RAG and how does retrieval-augmented generation compare with
other methods for reducing hallucinations in large language models?
Explain the differences between RAG, knowledge grounding, and
external knowledge retrieval.
"""


result = workflow.invoke({
    "original_query": user_query,
    "analysis": None,
    "expansion": None,
    "decomposition": None,
})


print("\n--- FINAL STATE ---")

print("\nOriginal Query:")
print(result["original_query"])

print("\nAnalysis:")
print(result["analysis"])

print("\nExpansion:")
print(result["expansion"])

print("\nDecomposition:")
print(result["decomposition"])