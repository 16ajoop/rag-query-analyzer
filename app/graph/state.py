from typing import TypedDict

from models.query_analysis import QueryAnalysis
from models.query_expansion import QueryExpansion
from models.query_decomposition import QueryDecomposition

class RAGState(TypedDict):
    original_query: str
    analysis: QueryAnalysis | None
    expansion: QueryExpansion | None
    decomposition: QueryDecomposition | None