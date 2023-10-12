import math
import nltk
import os
from logic_strategy import normalize_text, folder_path, documents_after_logic_search, delete_conjunctions, \
    tokenize_query

files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


# поиск инверсной частоты элемента запроса element
def find_inverse_frequency(term: str) -> float:
    file_count = 0
    for file in os.listdir(folder_path):
        file_contents = get_file_contents(file)
        normalized_text = [tag[0] for tag in normalize_text(nltk.word_tokenize(file_contents))]
        if term in file_contents:
            file_count += 1
        elif term in normalized_text:
            file_count += 1
    inverse_frequency = math.log(len(files)/file_count)
    return inverse_frequency


def find_weights_of_query_elements(tokenized_query: list, file_contents: str) -> dict:
    weights = {}
    normalized_text = [tag[0] for tag in normalize_text(nltk.word_tokenize(file_contents))]
    for term in delete_conjunctions(tokenized_query):
        if " " in term:
            term_local_frequency = file_contents.count(term)/len(file_contents.split())
        else:
            term_local_frequency = normalized_text.count(term)/len(normalized_text)
        weight = term_local_frequency * find_inverse_frequency(term)
        weights.update({term: weight})
    return weights


def get_file_contents(file_name: str) -> str:
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_contents = f.read()
                return file_contents
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {str(e)}")


def get_sorted_relevant_docs(tokenized_query: list) -> list:
    docs = documents_after_logic_search(tokenized_query)
    docs_for_sorting = {}
    for file in docs:
        file_contents = get_file_contents(file)
        docs_for_sorting.update({file: sum(find_weights_of_query_elements(tokenized_query, file_contents).values())})
    sorted_docs = sorted(docs_for_sorting.items(), key=lambda item: item[1], reverse=True)
    return [doc[0] for doc in sorted_docs]


if __name__ == "__main__":
    string = '"red roses" or "new document about"'
    # text = 'red roses'
    query = tokenize_query(string)
    print(get_sorted_relevant_docs(query))
    # print(find_inverse_frequency(['roses', 'new document about']))

