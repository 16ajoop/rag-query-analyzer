from chains.query_decomposition_chain import query_decomposition_chain


user_query = (
    "Compare RAG, RLHF, and DPO for reducing hallucinations "
    "and identify which approach has the strongest experimental evidence."
)


decomposition = query_decomposition_chain.invoke({
    "query": user_query
})


print("\n--- QUERY DECOMPOSITION ---")
print("Original Query:", decomposition.original_query)
print("Sub Queries:")

for query in decomposition.sub_queries:
    print("-", query)