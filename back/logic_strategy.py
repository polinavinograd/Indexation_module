import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import os

folder_path = "../texts"

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# ключевые слова поиска, подлежащие удалению
removable_tokens = ["find", "document", 'article', 'text', 'papers', "information", "data", "be"]

lemmatizer = WordNetLemmatizer()


# токенизация точных формулировок из запроса:
# In: '"red roses" or "new document about"'
# Out: ['red roses', 'or', 'new document about']
def exact_wording(input_string: str) -> list:
    tokenized_query = [s.strip('"') for s in re.findall(r'"[^"]*"|\S+', input_string.lower())]
    return tokenized_query


# нормализация (лемматизация) текста
def normalize_text(tokenized_query: list) -> list:
    part_of_speech_tags = nltk.pos_tag(tokenized_query)
    new_part_of_speech_tags = []
    for tag in part_of_speech_tags:
        wn_part_of_speech = wordnet.ADJ
        if tag[1].startswith('N'):
            wn_part_of_speech = wordnet.NOUN
        elif tag[1].startswith('V'):
            wn_part_of_speech = wordnet.VERB
        elif tag[1].startswith('R'):
            wn_part_of_speech = wordnet.ADV
        new_tag = tuple([lemmatizer.lemmatize(tag[0], wn_part_of_speech), tag[1]])
        new_part_of_speech_tags.append(new_tag)
    return new_part_of_speech_tags


# удаление вспомогательных частей речи(кроме союзов) и ключевых слов поиска
def remove_tokens(normalized_tags: list, need_to_remove_keywords: bool = False) -> list:
    result_text = []
    for tag in normalized_tags:
        if tag[1][0] not in ['V', 'N', 'R', 'J', 'C']:
            continue
        if need_to_remove_keywords:
            if tag[0] not in removable_tokens:
                result_text.append(tag[0] if tag[0] != 'but' else "and")
    return result_text


# удаление союзов из запроса для process_text(query)
def delete_conjunctions(tokenized_query: list):
    result_query = [term for term in tokenized_query if term not in ['and', 'or', 'not']]
    return result_query


def check_tokens_in_text(tokenized_query: list, file_contents: str) -> dict:
    res = {}
    added_terms = set()
    for term in tokenized_query:
        if file_contents.find(term) != -1:
            res.update({term: True})
            added_terms.add(term)
    not_added_terms = list(set(tokenized_query).difference(added_terms))
    file_contents = [tag[0] for tag in normalize_text(nltk.word_tokenize(file_contents))]
    for term in not_added_terms:
        if term in file_contents:
            res.update({term: True})
        else:
            res.update({term: False})
    return res


def tokenize_query(input_string: str) -> list:
    if input_string.count('"') > 1:
        tokenized_query = remove_tokens(normalize_text(exact_wording(input_string)), True)
    else:
        tokenized_query = remove_tokens(normalize_text(nltk.word_tokenize(input_string)), True)
    return tokenized_query


def check_logic_strategy(file_contents: str, tokenized_query: list):
    tokenized_query_without_conjunctions = delete_conjunctions(tokenized_query)
    query_dict = check_tokens_in_text(tokenized_query_without_conjunctions, file_contents)
    prev_word = ""
    res = {}
    or_statements = []
    for word in tokenized_query:
        if word not in ['and', 'or', 'not']:
            if prev_word != 'not':
                if prev_word == 'or':
                    or_statements.append(word)
                else:
                    res.update({word: True})
            else:
                res.update({word: False})
        elif word == 'or':
            or_statements.append(prev_word)
        prev_word = word

    for key in res.keys():
        if res[key] != query_dict[key]:
            return False
    return any(query_dict[term] for term in or_statements) if len(or_statements) != 0 else True


def documents_after_logic_search(tokenized_query: list) -> list:
    relevant_docs = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_contents = f.read()
                    if check_logic_strategy(file_contents, tokenized_query):
                        relevant_docs.append(file)
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {str(e)}")
    return relevant_docs


if __name__ == "__main__":
    # text = 'bees flowers'
    # text = 'bees flowers roses'
    # string = "find documents where there is information about bees and flowers but not about roses"

    string = '"red roses" or "new document about"'
    text = 'red roses'
    print(documents_after_logic_search(tokenize_query(string)))
    # text = 'roses are red'
    # text = 'new roses'

