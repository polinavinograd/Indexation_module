import nltk
from natural_language_utils import NaturalLanguageUtils
import datetime


class Document:
    REMOVABLE_TOKENS = ["find", "document", 'article', 'text', 'papers', "information", "data", "be"]

    def __init__(self, name: str, text: str, creation_datetime: datetime.datetime):
        self.name = name
        self.text = text.lower()
        self.creation_datetime = creation_datetime

    def tokenized(self) -> 'list[str]':
        return nltk.word_tokenize(self.text)

    def normalized(self) -> 'list[str]':
        return NaturalLanguageUtils.normalize_tokens_only(self.tokenized())
    
    def has_token(self, token: str) -> bool:
        return token in self.normalized() or self.text.find(token) != -1
    
    def has_tokens(self, tokens: 'list[str]') -> 'dict[str, bool]':
        TOKEN_PRESENCE_MAP = {}

        for token in tokens:
            TOKEN_PRESENCE_MAP.update({ token: self.has_token(token) })

        return TOKEN_PRESENCE_MAP

    def get_word_count(self) -> int:
        return len(self.text.split())

    # удаление вспомогательных частей речи (кроме союзов) и ключевых слов поиска
    def stripped_from_excessive_tokens(self, need_to_remove_keywords: bool = True) -> 'list[str]':
        resulting_tag_list = []
        for tag in NaturalLanguageUtils.normalize(self.tokenized()):
            if tag[1][0] not in ['V', 'N', 'R', 'J']:
                continue
            if need_to_remove_keywords:
                if tag[0] not in self.REMOVABLE_TOKENS:
                    resulting_tag_list.append(tag[0] if tag[0] != 'but' else "and")

        return resulting_tag_list
