import math
from document import Document
from search_query import SearchQuery
from document_storage import DocumentStorage
from natural_language_utils import NaturalLanguageUtils

class IndexationModule:
    TOKEN_WEIGHTS = {}

    def __init__(self, document_storage: DocumentStorage):
        self.document_list = document_storage.get_all_documents()
        for document in self.document_list:
            for token in NaturalLanguageUtils.normalize_tokens_only(document.tokenized()):
                if (self.TOKEN_WEIGHTS[token] is None):
                    self.TOKEN_WEIGHTS[token] = 0
                self.TOKEN_WEIGHTS[token] += self.get_token_weight(token, document, self.document_list)

    def get_inverse_frequency(self, token: str, document_list: 'list[Document]') -> float:
        DOCS_THAT_HAVE_TOKEN = list(filter(lambda document: document.has_token(token), document_list))
        return math.log(len(document_list) / (len(DOCS_THAT_HAVE_TOKEN) + 1))

    def get_token_weight(self, token: str, document: Document, document_list: 'list[Document]') -> float:
        LIST_TO_LOOK_FOR_TOKEN_IN = document.text if " " in token else document.normalized()
        return self.get_inverse_frequency(token, document_list) * (LIST_TO_LOOK_FOR_TOKEN_IN.count(token) / document.get_word_count())

    def get_token_weights(self, tokens: 'list[str]', document: Document, document_list: 'list[Document]') -> 'dict[str, float]':
        TOKEN_WEIGHTS = {}

        for token in tokens:
            TOKEN_WEIGHT = self.get_token_weight(token, document, document_list)
            synonyms_combined_weight = 0
            for SYNONYM in NaturalLanguageUtils.synonyms(token):
                synonyms_combined_weight += self.get_token_weight(SYNONYM, document, document_list)
            TOKEN_WEIGHTS[token] = TOKEN_WEIGHT + synonyms_combined_weight

        return TOKEN_WEIGHTS

    def get_doc_relevance(self, query: SearchQuery, document: Document, document_list: 'list[Document]') -> float:
        relevance = 0

        for token in query.normalized():
            relevance += self.TOKEN_WEIGHTS[token]

        return relevance