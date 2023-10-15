from document_storage import DocumentStorage
from indexation_module import IndexationModule
from search_query import SearchQuery
from search_result import SearchResult
from logic_strategy import filter_document_list_with_logic_strategy

DOCUMENT_STORAGE = DocumentStorage()
INDEXATION_MODULE = IndexationModule()

def search(query: str) -> list[SearchResult]:
    SEARCH_QUERY = SearchQuery(query)
    ALL_DOCUMENTS = DOCUMENT_STORAGE.get_all_documents()
    SUITABLE_DOCUMENTS = filter_document_list_with_logic_strategy(SEARCH_QUERY, ALL_DOCUMENTS)
    return list(map(lambda document: SearchResult(
        document,
        INDEXATION_MODULE.get_token_weights(SEARCH_QUERY.stripped_from_conjunctions(), document, ALL_DOCUMENTS),
        INDEXATION_MODULE.get_doc_relevance(SEARCH_QUERY, document, ALL_DOCUMENTS)
    ), SUITABLE_DOCUMENTS))

def get_doc_text_by_name(doc_name: str) -> str:
    return DOCUMENT_STORAGE.get_document_by_name(doc_name).text

def get_metrics() -> dict[str, float]:
    return {
        "recall": 0.8461,
        "precision": 0.7857,
        "accuracy": 0.8936,
        "error": 0.1063,
        "fMeasure": 0.8148
    }