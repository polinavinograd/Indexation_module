import math
from document import Document
from search_query import SearchQuery

# to be intellectualzied (?)
class IndexationModule:
    def __init__(self):
        pass

    def get_inverse_frequency(self, token: str, document_list: list[Document]) -> float:
        DOCS_THAT_HAVE_TOKEN = list(filter(lambda document: document.has_token(token), document_list))
        return math.log(len(document_list) / len(DOCS_THAT_HAVE_TOKEN))

    def get_token_weight(self, token: str, document: Document, document_list: list[Document]) -> float:
        LIST_TO_LOOK_FOR_TOKEN_IN = document.text if " " in token else document.normalized()
        return self.get_inverse_frequency(token, document_list) * (LIST_TO_LOOK_FOR_TOKEN_IN.count(token) / document.get_word_count())

    def get_token_weights(self, tokens: list[str], document: Document, document_list: list[Document]) -> dict[str, float]:
        return dict(zip(
            tokens,
            list(map(lambda token: self.get_token_weight(token, document, document_list), tokens))
        ))

    def get_doc_relevance(self, query: SearchQuery, document: Document, document_list: list[Document]) -> float:
        relevance = 0

        QUERY_TOKEN_WEIGHTS = self.get_token_weights(query.stripped_from_conjunctions(), document, document_list)
        for token in QUERY_TOKEN_WEIGHTS:
            relevance += QUERY_TOKEN_WEIGHTS[token]

        return relevance