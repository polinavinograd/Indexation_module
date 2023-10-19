import nltk
from nltk.corpus import wordnet
from nltk import WordNetLemmatizer

LEMMATIZER = WordNetLemmatizer()

class NaturalLanguageUtils:
    @staticmethod
    def normalize(tokenized_text: 'list[str]') -> list:
        part_of_speech_tags = nltk.pos_tag(tokenized_text)
        new_part_of_speech_tags = []
        for tag in part_of_speech_tags:
            wn_part_of_speech = wordnet.ADJ
            if tag[1].startswith('N'):
                wn_part_of_speech = wordnet.NOUN
            elif tag[1].startswith('V'):
                wn_part_of_speech = wordnet.VERB
            elif tag[1].startswith('R'):
                wn_part_of_speech = wordnet.ADV
            new_tag = tuple([LEMMATIZER.lemmatize(tag[0], wn_part_of_speech), tag[1]])
            new_part_of_speech_tags.append(new_tag)
        return new_part_of_speech_tags
    
    @staticmethod
    def normalize_tokens_only(tokenized_text: 'list[str]') -> 'list[str]':
        return list(map(lambda tag: tag[0], NaturalLanguageUtils.normalize(tokenized_text)))
    
    @staticmethod
    def synonyms(word: str, max_synonyms: int = 3) -> 'list[str]':
        SYNONYMS = []

        synonyms_found = 0
        for synset in wordnet.synsets(word):
            for lemma in synset.lemmas():
                if lemma.name() in SYNONYMS or lemma.name() == word:
                    continue
                SYNONYMS.append(lemma.name())
                synonyms_found += 1
                if synonyms_found == max_synonyms:
                    break
            if synonyms_found == max_synonyms:
                    break

        return SYNONYMS