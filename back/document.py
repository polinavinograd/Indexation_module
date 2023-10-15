import nltk
from natural_language_utils import NaturalLanguageUtils
import datetime

class Document:
    def __init__(self, name: str, text: str, creation_datetime: datetime.datetime):
        self.name = name
        self.text = text
        self.creation_datetime = creation_datetime

    def tokenized(self) -> list[str]:
        return nltk.word_tokenize(self.text)

    def normalized(self) -> list[str]:
        return NaturalLanguageUtils.normalize_tokens_only(self.tokenized())
    
    def has_token(self, token: str) -> bool:
        return self.text.find(token) != -1 or token in self.normalized()
    
    def has_tokens(self, tokens: list[str]) -> dict[str, bool]:
        TOKEN_PRESENCE_MAP = {}

        for token in tokens:
            TOKEN_PRESENCE_MAP.update({ token: self.has_token(token) })

        return TOKEN_PRESENCE_MAP

    def get_word_count(self) -> int:
        return len(self.text.split())