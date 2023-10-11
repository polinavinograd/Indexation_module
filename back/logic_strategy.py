import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
import re

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# ключевые слова поиска, подлежащие удалению
removable_tokens = ["find", "document", 'article', 'text', 'papers', "information", "data", "be"]
lemmatizer = WordNetLemmatizer()


# токенизация точных формулировок из запроса:
# In: '"red roses" or "new document about"'
# Out: ['red roses', 'or', 'new document about']
def exact_wording(query: str) -> list:
    tokenized = [s.strip('"') for s in re.findall(r'"[^"]*"|\S+', query.lower())]
    return tokenized


# нормализация (лемматизация) текста
def normalize_text(tokenized: list) -> list:
    pos_tags = nltk.pos_tag(tokenized)
    new_pos_tags = []
    for tag in pos_tags:
        wn_pos = wordnet.ADJ
        if tag[1].startswith('N'):
            wn_pos = wordnet.NOUN
        elif tag[1].startswith('V'):
            wn_pos = wordnet.VERB
        elif tag[1].startswith('R'):
            wn_pos = wordnet.ADV
        new_tag = tuple([lemmatizer.lemmatize(tag[0], wn_pos), tag[1]])
        new_pos_tags.append(new_tag)
    return new_pos_tags


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
def delete_conjunctions(query: list):
    res = [el for el in query if el not in ['and', 'or', 'not']]
    return res


def process_text(query: list, text: str) -> dict:
    res = {}
    added_keys = set()
    for el in query:
        if text.find(el) != -1:
            res.update({el: True})
            added_keys.add(el)
    not_added_keys = list(set(query).difference(added_keys))
    tokenized = nltk.word_tokenize(text)
    text = [tag[0] for tag in normalize_text(tokenized)]
    for key in not_added_keys:
        if key in text:
            res.update({key: True})
        else:
            res.update({key: False})
    return res


def check_logic_strategy(text: str, query: str):
    if query.count('"') > 1:
        tokenized_query = remove_tokens(normalize_text(exact_wording(query)), True)
    else:
        tokenized = nltk.word_tokenize(query)
        tokenized_query = remove_tokens(normalize_text(tokenized), True)

    tokenized_query_without_conjunctions = delete_conjunctions(tokenized_query)
    text_dict = process_text(tokenized_query_without_conjunctions, text)
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
        if res[key] != text_dict[key]:
            return False
    return any(text_dict[key] is True for key in or_statements) if len(or_statements) != 0 else True


if __name__ == "__main__":
    # text = 'bees flowers'
    # text = 'bees flowers roses'
    # string = "find documents where there is information about bees and flowers but not about roses"

    string = '"red roses" or "new document about"'
    text = 'red roses'
    # text = 'roses are red'
    # text = 'new roses'

    print(check_logic_strategy(text, string))
