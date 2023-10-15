import re
import nltk
from natural_language_utils import NaturalLanguageUtils

class SearchQuery:
    REMOVABLE_TOKENS = ["find", "document", 'article', 'text', 'papers', "information", "data", "be"]

    def __init__(self, query):
        self.query = query

    # выделение точных формулировок из запроса
    # In: '"red roses" or "new document about"'
    # Out: ['red roses', 'or', 'new document about']
    def get_exact_wording(self) -> list[str]:
        return [s.strip('"') for s in re.findall(r'"[^"]*"|\S+', self.query.lower())]
    
    # токенизация запроса
    def tokenized(self) -> list[str]:
        if self.query.count('"') > 1:
            return self.get_exact_wording()
        else:
            return nltk.word_tokenize(self.query)
    
    # нормализация (лемматизация) запроса
    def normalized(self) -> list[str]:
        return NaturalLanguageUtils.normalize_tokens_only(self.tokenized())
    
    # удаление вспомогательных частей речи (кроме союзов) и ключевых слов поиска
    def stripped_from_excessive_tokens(self, need_to_remove_keywords: bool = True) -> list[str]:
        resulting_tag_list = []
        for tag in NaturalLanguageUtils.normalize(self.tokenized()):
            if tag[1][0] not in ['V', 'N', 'R', 'J', 'C']:
                continue
            if need_to_remove_keywords:
                if tag[0] not in self.REMOVABLE_TOKENS:
                    resulting_tag_list.append(tag[0] if tag[0] != 'but' else "and")
        
        return resulting_tag_list
    
    # удаление союзов из запроса
    def stripped_from_conjunctions(self) -> list[str]:
        return [term for term in self.stripped_from_excessive_tokens() if term not in ['and', 'or', 'not']]