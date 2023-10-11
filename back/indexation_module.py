import math
import nltk
from logic_strategy import normalize_text, remove_tokens
import os

folder_path = "../texts"
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


def process_text(text: str) -> list:
    tokenized = nltk.word_tokenize(text)
    tokenized = remove_tokens(normalize_text(tokenized))
    return tokenized


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


# есть 2 вида нормализованных терминов:
# либо строка из нескольких слов "red roses" - если ищется конкретная формулировка,
# либо одно слово в начальной форме: "rose"
#
# нужно посчитать вхождение термина в документ
#
# считать вхождения в ненормализованный текст недостаточно, т.к. есть использования термина в неначальной форме,
# которые тоже считаются
# считать вхождения в нормализованный текст проблемно из-за наличия "конкретных формулировок из нескольких слов"
# - в нормализованном тексте их будет 0
def find_weights(query: list, text:str):
    weights = {}
    for element in query:
        norm_text = [tag[0] for tag in normalize_text(nltk.word_tokenize(text))]
        if element in text:
            q = text.count(element)/len(text.split())
        if element in norm_text:
            q = norm_text.count(element)/len(norm_text)
        weight = q * find_inverse_frequency(element)
        weights.update({element: weight})
    return weights


if __name__ == "__main__":
    pass
    # print(find_inverse_frequency(['roses', 'new document about']))

