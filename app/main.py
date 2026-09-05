from graph.workflow import workflow


user_query = "What is RAG and how does it reduce hallucinations in LLMs?"


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