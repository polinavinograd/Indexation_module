from document import Document
from search_query import SearchQuery

def logic_search_strategy(query: SearchQuery, document: Document) -> bool:
    query_without_conjunctions = query.stripped_from_conjunctions()
    query_dict = document.has_tokens(query_without_conjunctions)
    prev_word = ""
    word_presence_map = {}
    or_statements = []
    for word in query.stripped_from_excessive_tokens():
        if word not in ['and', 'or', 'not']:
            if prev_word != 'not':
                if prev_word == 'or':
                    or_statements.append(word)
                else:
                    word_presence_map.update({ word: True })
            else:
                word_presence_map.update({ word: False })
        elif word == 'or':
            or_statements.append(prev_word)
        prev_word = word

    for key in word_presence_map.keys():
        if word_presence_map[key] != query_dict[key]:
            return False
    return any(query_dict[term] for term in or_statements) if len(or_statements) != 0 else True

def filter_document_list_with_logic_strategy(query: SearchQuery, document_list: list[Document]) -> list[Document]:
    return list(filter(lambda document: logic_search_strategy(query, document), document_list))