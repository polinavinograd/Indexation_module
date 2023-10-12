from logic_strategy import tokenize_query
from indexation_module import get_sorted_relevant_docs


def search(input_string: str) -> list:
    return get_sorted_relevant_docs(tokenize_query(input_string))