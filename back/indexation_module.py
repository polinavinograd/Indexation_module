import math
import json
from document import Document
from search_query import SearchQuery
from document_storage import DocumentStorage
from natural_language_utils import NaturalLanguageUtils


class IndexationModule:
    def __init__(self, document_storage):
        with open('index.json', 'r+') as file:
            try:
                self.index = json.load(file)
            except json.JSONDecodeError:
                self.index = {}
                all_docs = document_storage.get_all_documents()
                for document in all_docs:
                    self.index.update({document.name: self.get_token_weights(document.stripped_from_excessive_tokens(),
                                                                             document, all_docs)})
                json.dump(self.index, file, indent=4)

    @staticmethod
    def get_inverse_frequency(token: str, document_list: 'list[Document]') -> float:
        DOCS_THAT_HAVE_TOKEN = list(filter(lambda document: document.has_token(token), document_list))
        return math.log(len(document_list) / (len(DOCS_THAT_HAVE_TOKEN) + 1))

    def get_token_weight(self, token: str, document: Document, document_list: 'list[Document]') -> float:
        LIST_TO_LOOK_FOR_TOKEN_IN = document.text if " " in token else document.normalized()
        return self.get_inverse_frequency(token, document_list) * (LIST_TO_LOOK_FOR_TOKEN_IN.count(token) /
                                                                   document.get_word_count())

    def get_token_weights(self, tokens: 'list[str]', document: Document, document_list: 'list[Document]') -> 'dict[str, float]':
        TOKEN_WEIGHTS = {}

        for token in tokens:
            TOKEN_WEIGHT = self.get_token_weight(token, document, document_list)
            synonyms_combined_weight = 0
            for SYNONYM in NaturalLanguageUtils.synonyms(token):
                synonyms_combined_weight += self.get_token_weight(SYNONYM, document, document_list)
            TOKEN_WEIGHTS[token] = TOKEN_WEIGHT + synonyms_combined_weight

        return TOKEN_WEIGHTS

    # def get_doc_relevance(self, query: SearchQuery, document: Document, document_list: list[Document]) -> float:
    #     relevance = 0
    #
    #     QUERY_TOKEN_WEIGHTS = self.get_token_weights(query.stripped_from_conjunctions(), document, document_list)
    #     for token in QUERY_TOKEN_WEIGHTS:
    #         relevance += QUERY_TOKEN_WEIGHTS[token]
    #
    #     return relevance
