import math
import nltk
from logic_strategy import normalize_text, folder_path, documents_after_logic_search, delete_conjunctions, tokenize_query
import os

files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


# поиск инверсной частоты элемента запроса element
def find_inverse_frequency(element: str) -> float:
    file_count = 0
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_contents = f.read()
                    text = [tag[0] for tag in normalize_text(nltk.word_tokenize(file_contents))]
                    if element in file_contents:
                        file_count += 1
                    elif element in text:
                        file_count += 1
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {str(e)}")
    inverse_frequency = math.log(len(files)/file_count)
    return inverse_frequency


# поиск весов элементов запроса
def find_weights_of_query_elements(query: list, text: str) -> dict:
    weights = {}
    for element in delete_conjunctions(query):
        norm_text = [tag[0] for tag in normalize_text(nltk.word_tokenize(text))]
        if " " in element:
            q = text.count(element)/len(text.split())
        else:
            q = norm_text.count(element)/len(norm_text)
        weight = q * find_inverse_frequency(element)
        weights.update({element: weight})
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


def get_sorted_relevant_docs(query: list) -> list:
    docs = documents_after_logic_search(query)
    docs_for_sorting = {}
    for file in docs:
        text = get_file_contents(file)
        docs_for_sorting.update({file: sum(find_weights_of_query_elements(query, text).values())})
    sorted_docs = sorted(docs_for_sorting.items(), key=lambda item: item[1], reverse=True)
    return [doc[0] for doc in sorted_docs]


if __name__ == "__main__":
    string = '"red roses" or "new document about"'
    text = 'red roses'
    query = tokenize_query(string)
    print(get_sorted_relevant_docs(query))
    # print(find_inverse_frequency(['roses', 'new document about']))

