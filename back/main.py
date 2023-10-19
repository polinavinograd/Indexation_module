from document_storage import DocumentStorage
from indexation_module import IndexationModule
from search_query import SearchQuery
from search_result import SearchResult
from logic_strategy import filter_document_list_with_logic_strategy

DOCUMENT_STORAGE = DocumentStorage()
INDEXATION_MODULE = IndexationModule(DOCUMENT_STORAGE)

def search(query: str) -> 'list[SearchResult]':
    SEARCH_QUERY = SearchQuery(query)
    ALL_DOCUMENTS = DOCUMENT_STORAGE.get_all_documents()
    SUITABLE_DOCUMENTS = filter_document_list_with_logic_strategy(SEARCH_QUERY, ALL_DOCUMENTS)
    result = list()
    for doc in SUITABLE_DOCUMENTS:
        top_words = {}
        relevance = 0
        for token in SEARCH_QUERY.stripped_from_conjunctions():
            if token in INDEXATION_MODULE.index[doc.name].keys():
                weight = INDEXATION_MODULE.index[doc.name][token]
            else:
                weight = 0
            top_words.update({token: weight})
            relevance += weight
        result.append(SearchResult(doc, top_words, relevance))
    return result

def get_doc_text_by_name(doc_name: str) -> str:
    return DOCUMENT_STORAGE.get_document_by_name(doc_name).text

def get_metrics() -> 'dict[str, float]':
    return {
        "recall": 0.8461,
        "precision": 0.7857,
        "accuracy": 0.8936,
        "error": 0.1063,
        "fMeasure": 0.8148
    }