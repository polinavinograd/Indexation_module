from document import Document

class SearchResult:
    def __init__(self, document: Document, top_words: 'dict[str, float]', relevance: float):
        self.document = document
        self.relevance = relevance
        self.top_words = top_words